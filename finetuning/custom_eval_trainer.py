import collections
import json
import os
from pathlib import Path

import wandb
import yaml
from lm_eval import evaluator
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
        eval_harness_cfg = "configs/evaluate/eval_args.yaml",
    ):
        super().__init__(model, args, data_collator, train_dataset, eval_dataset, tokenizer, model_init, compute_metrics, callbacks, optimizers)
        with open(eval_harness_cfg, "r") as f:
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

        # Additionally perform lm-evaluation-harness evaluations

        # Eval harness requires a saved HF transformers model as input, so we save to file and pass that as input
        eval_model_path = Path(self.args.output_dir) / f"eval_harness_model-{self.state.global_step}"
        self.save_model(eval_model_path)
        print("Saved to ", eval_model_path)
        self.eval_harness_args['model_args'] = f"pretrained={str(eval_model_path)}"
        os.remove(eval_model_path / "pytorch_model.bin") # Don't waste space

        eval_output = evaluator.simple_evaluate(**self.eval_harness_args)

        # Merge only results from the HF evaluation and LM Eval Harness
        results_dict['dev'] = eval_output['results']
        wandb.log(results_dict)

        # Log all data to file
        with open(eval_model_path / "eval_output.json", "w") as f:
            dumped = json.dumps(results_dict, indent=2)
            f.write(dumped)
        
        print(results_dict)
        return flatten(results_dict) # Metrics expects a flat 1-level dict
