import argparse
import json
import sys
from pathlib import Path

import wandb

from common import utils
from dataset import build_dataset
from finetuning import run_clm


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finetune model with dataset')
    parser.add_argument("-d", "--dataset-config", required=True, help="Dataset config file")
    parser.add_argument("-m", "--model", help="Base model name (must be a causal-lm model on HuggingFace)")
    parser.add_argument("-f", "--finetune-config-base", help="Base for finetune config file")
    options = parser.parse_args()

    # Build dataset
    dataset_cfg = utils.load_config(options.dataset_config)
    build_dataset.main(dataset_cfg)

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
        dataset_path = str(Path(dataset_cfg['output_dir']) / dataset_cfg['unique_name'] / "data")
        update_cfg = {
            'model_name_or_path': options.model,
            'dataset_name': dataset_path,
            'output_dir': str(out_dir),
            'run_name': wandb.run.name,
        }
        finetune_cfg.update(update_cfg)
        print(finetune_cfg)

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
    })

    # We need to override the sys arguments to pass the finetune config to run_clm
    sys.argv = [sys.argv[0], new_finetune_cfg_path]
    run_clm.main()
