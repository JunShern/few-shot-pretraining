# Few-shot Pretraining

## Install
```bash
conda create -n alignment python=3.8
conda activate alignment
python -m pip install -r requirements.txt
```

## Download base datasets
```bash
# Need at least 2TB of free space for full downloads!
./dataset/scripts/download_pile.py
./dataset/scripts/download_c4.py
```

## (optional) Log in to WANDB
To track experiments, log in to Weights & Biases:
```
wandb login # Follow the link to grab the API key
```

## Quickstart

Run one-liner to generate a dataset (or reuse if already exists) and finetune a model on it:
```bash
python finetune_with_dataset.py \
	-d configs/dataset/AllDocuments_1k.yaml \
	-f configs/finetune/default.json \
	-m EleutherAI/gpt-neo-125M
```

The above should produce the following outputs:
```bash
output/
├── datasets                                        # Generated finetuning datasets
│   └── AllDocuments_1k                             # - Datasets are identified by `unique_name`
└── models                                          # Saved model checkpoints and logs
    └── EleutherAI.gpt-neo-125M_rosy-elevator-39    # - Each run generates a new model folder
```

## Beyond the defaults

Each full run consists of a build-dataset phase and a finetune phase.
- The build-dataset phase is configured via a dataset config file (see `configs/dataset` for examples). You can generate a dataset (without the finetuning step) directly:
	```
	python dataset/build_dataset.py -c configs/dataset/AllDocuments_1k.yaml
	```
- The finetune phase is configured via a finetune config file (see `configs/finetune` for examples)


To customize a run to your liking, modify the relevant config files / create new config files.


## (Optional) Browse the generated dataset
```bash
streamlit run streamlit/browse_dataset.py -- --data-dir output/dataset/AllDocuments_1k
```

## (Advanced) Hyperparameter sweeps
```bash
# Initialize sweep
wandb sweep -e junshern -p alignment_pretraining configs/finetune/hyper_search/sweep.yaml

# Manually edit the sweep_agent.sbatch file:
# - Update SWEEPID in `wandb agent --count 1 junshern/alignment_pretraining/SWEEPID`
# - Request the correct NUM_ARR_JOBS to perform the sweep using `#SBATCH --array=1-NUM_ARR_JOBS`

# Run jobs
sbatch batch_jobs/hyper_search/sweep.sbatch
```