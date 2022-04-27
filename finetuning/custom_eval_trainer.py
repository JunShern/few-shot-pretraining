import collections
import json
import math
import numpy as np
import os
import time
from pathlib import Path

import wandb
import yaml
from lm_eval import evaluator, tasks
from transformers import Trainer


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class CustomEvalTrainer(Trainer):
    def __init__(
        self,
        model = None,
        args = None,
        data_collator = None,
        train_dataset = None,
        eval_dataset = None,
        tokenizer = None,
        model_init = None,
        compute_metrics = None,
        callbacks = None,
        optimizers = (None, None),
        eval_harness_cfg = None,
    ):
        super().__init__(model, args, data_collator, train_dataset, eval_dataset, tokenizer, model_init, compute_metrics, callbacks, optimizers)
        with open(eval_harness_cfg, "r") as f:
            print("Loading harness config file", eval_harness_cfg)
            self.eval_harness_args = yaml.safe_load(f)
        return

    def evaluate(
        self,
        eval_dataset = None,
        ignore_keys = None,
        metric_key_prefix = "eval",
    ):
        # Run the default LM loss evaluations
        results_dict = super().evaluate(eval_dataset, ignore_keys, metric_key_prefix)

        # Add perplexity loss
        try:
            perplexity = math.exp(results_dict["eval_loss"])
        except OverflowError:
            perplexity = float("inf")
        results_dict["perplexity"] = perplexity

        # Additionally perform lm-evaluation-harness evaluations

        # Eval harness requires a saved HF transformers model as input, so we save to file and pass that as input
        eval_model_path = Path(self.args.output_dir) / f"eval_harness_model-{self.state.global_step}"
        self.save_model(eval_model_path)
        print("Saved to ", eval_model_path)
        self.eval_harness_args['model_args'] = f"pretrained={str(eval_model_path)}"
        if not self.eval_harness_args['tasks']:
            all_tasks = tasks.ALL_TASKS
            if self.eval_harness_args['num_fewshot'] > 0: 
                blacklist = ['blimp', 'asdiv', 'truthfulqa', 'prost', 'wikitext', 'pile'] # blacklist tasks that are not designed for fewshot
                blacklist += ['coqa'] # coqa has some issues with gpt-2, see here: https://github.com/EleutherAI/lm-evaluation-harness/issues/238
                blacklist += ['squad2'] # squad2 seems to be missing a key `NoAns_exact` which is expected; this may be fixed in datasets==2.1.0 but lm-eval==0.2.0 requires datasets==1.14.1
                blacklist += ['hendrycks'] # Just cut some out because evaluation is taking too long right now
                # remove any tasks that contain (not full match) these strings
                all_tasks = [task for task in all_tasks if all([blacklist_item not in task for blacklist_item in blacklist])]
            self.eval_harness_args['tasks'] = [task for task in all_tasks]
        print(f"JS SAYS: Evaluating on {all_tasks}")
        print("JS SAYS: STARTING simple_evaluate")
        t_start = time.time()
        eval_output = evaluator.simple_evaluate(**self.eval_harness_args)
        print(f"JS SAYS: FINISHED simple_evaluate ({time.time() -  t_start}s)")
        # Add an aggregation of all the task accuracies for evaluation
        list_of_acc = []
        list_of_acc_norm = []
        for key, val in eval_output['results'].items():
            if 'acc' in val:
                list_of_acc.append(val['acc'])
            if 'acc_norm' in val:
                list_of_acc_norm.append(val['acc_norm'])
        # # Craft a custom metric to balance our task selection
        # custom_metrics = [
        #     ('headqa', 'acc_norm'), 
        #     ('logiqa', 'acc_norm'),
        #     ('mathqa', 'acc_norm'),
        #     ('pubmedqa', 'acc'),
        #     ('qa4mre', 'acc_norm'),
        # ]
        # list_of_acc_custom = []
        # for metric_name, metric_type in custom_metrics:
        #     # We want to group similar metrics into one
        #     # e.g. 'qa4mre' should be the mean of 'qa4mre_2011', 'qa4mre_2012', 'qa4mre_2013'
        #     val = np.mean([val[metric_type] for key, val in eval_output['results'].items() if metric_name in key])
        #     list_of_acc_custom.append(val)

        eval_output['results']['aggregates'] = {
            'mean_acc': np.mean(list_of_acc),
            'mean_acc_norm': np.mean(list_of_acc_norm),
            # 'mean_acc_custom': np.mean(list_of_acc_custom),
        }

        # Merge only results from the HF evaluation and LM Eval Harness
        results_dict['dev'] = eval_output['results']
        results_dict['dev_acc'] = np.mean(list_of_acc)
        wandb.log(results_dict)

        # Log all data to file
        with open(eval_model_path / "eval_output.json", "w") as f:
            dumped = json.dumps(results_dict, indent=2)
            f.write(dumped)
        
        # Cleanup, don't waste space
        os.remove(eval_model_path / "pytorch_model.bin")

        print(results_dict)
        return flatten(results_dict) # Metrics expects a flat 1-level dict

    def log(self, logs):
        """
        Log :obj:`logs` on the various objects watching training.
        Subclass and override this method to inject custom behavior.
        Args:
            logs (:obj:`Dict[str, float]`):
                The values to log.
        """
        if self.state.epoch is None:
            logs["epoch"] = 0
        else:
            logs["epoch"] = round(self.state.epoch, 2)

        output = {**logs, **{"step": self.state.global_step}}
        self.state.log_history.append(output)
        self.control = self.callback_handler.on_log(self.args, self.state, self.control, logs)