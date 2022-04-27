import argparse
import json
import os
import sys
from pathlib import Path

import wandb

from common import utils
from dataset import build_dataset
from finetuning import run_clm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finetune model with dataset')
    parser.add_argument("-d", "--dataset-config", required=True, help="Dataset config file")
    parser.add_argument("-v", "--val-dataset-config", required=True, help="Validation dataset config file")
    parser.add_argument("-m", "--model", help="Base model name (must be a causal-lm model on HuggingFace)")
    parser.add_argument("-f", "--finetune-config-base", help="Base for finetune config file")
    options, unknown = parser.parse_known_args()

    # Build dataset
    dataset_cfg = utils.load_config(options.dataset_config)
    print("JS SAYS: Building train")
    build_dataset.main(dataset_cfg)
    val_dataset_cfg = utils.load_config(options.val_dataset_config)
    print("JS SAYS: Building val")
    build_dataset.main(val_dataset_cfg)
    # We need a plain text file version of the validation dataset
    val_file_path = Path(val_dataset_cfg['output_dir']) / val_dataset_cfg['unique_name'] / 'data/val.txt'
    if not val_file_path.exists():
        val_file_path_jsonl = Path(val_dataset_cfg['output_dir']) / val_dataset_cfg['unique_name'] / "data/data.jsonl"
        with open(val_file_path_jsonl) as f:
            with open(val_file_path, 'w') as f_out:
                for line in f.readlines():
                    obj = json.loads(line)
                    f_out.write(obj['text'])
    
    print("JS SAYS: Finished building")

    if options.finetune_config_base is None:
        print("No finetune script specified, exiting.")
        sys.exit()
    if options.model is None:
        print("No model specified, exiting.")
        sys.exit()

    # Setup wandb logging
    wandb.init(
        project="alignment_pretraining",
        # mode='disabled',
    )
    wandb.run.name = f"{options.model}_{dataset_cfg['unique_name']}_{wandb.run.name}".replace('/', '.')
    out_dir = Path("./output/models") / wandb.run.name
    out_dir.mkdir(parents=True)
    print(f"Kicking off run: {wandb.run.name}")

    # Patch the finetune config file with the requested dataset + model
    with open(options.finetune_config_base, 'r') as f:
        finetune_cfg = json.load(f)
        dataset_path = Path(dataset_cfg['output_dir']) / dataset_cfg['unique_name'] / "data"
        update_cfg = {
            'model_name_or_path': options.model,
            'dataset_name': str(dataset_path),
            'output_dir': str(out_dir),
            'run_name': wandb.run.name,
            'validation_file': str(val_file_path),
        }
        finetune_cfg.update(update_cfg)
        print(finetune_cfg)

    # Some parameters populated with wandb sweeps
    for key, val in finetune_cfg.items():
        if val == 'SWEEP_PARAM':
            # Retrieve the current sweep parameter (populated by wandb)
            finetune_cfg[key] = wandb.config[key]

    # Save configs to the output directory
    (out_dir / "configs").mkdir(parents=True)
    new_finetune_cfg_path = str(out_dir / "configs/finetune.json")
    new_dataset_cfg_path = str(out_dir / "configs/dataset.yaml")
    with open(new_finetune_cfg_path, 'w') as f:
        json.dump(finetune_cfg, f, indent=4, sort_keys=True)
    with open(new_dataset_cfg_path, 'w') as f:
        json.dump(dataset_cfg, f, indent=4, sort_keys=True)

    # Log configs
    wandb.config.update({
        'dataset': dataset_cfg,
        'finetune': finetune_cfg,
        'slurm_job_id': os.environ['SLURM_JOB_ID'] if 'SLURM_JOB_ID' in os.environ else '',
    })

    # We need to override the sys arguments to pass the finetune config to run_clm
    sys.argv = [sys.argv[0], new_finetune_cfg_path]
    run_clm.main()
