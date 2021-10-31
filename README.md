# Few-shot Pretraining

## Install
```bash
conda create -n alignment python=3.8
conda activate alignment
python -m pip install -r requirements.txt
```

## Quickstart

Run one-liner:
```bash
./run_full_pipeline.sh
```

The above should produce the following outputs:
```bash
output/
└── ExampleStringsCriterion_10k/
	├── configs/					# Copy of the configs used for this run
	├── dataset/					# The generated finetuning dataset
	└── model/						# Saved model checkpoints and logs
```

## Beyond the defaults

Each full run consists of a build-dataset phase and a finetune phase.
- The build-dataset phase is configured via a dataset config file (see `configs/dataset` for examples)
- The finetune phase is configured via a finetune config file (see `configs/finetune` for examples)

To customize a run to your liking, modify the relevant config files / create new config files.

See `run_full_pipeline.sh` to understand how the pipeline works.

Alternatively, you can run each phase of the pipeline manually:
```bash
# Build a small test dataset:
python dataset/build_dataset.py -c configs/dataset/ExamplesStringsCriterion_10k.yaml
# (Optional) Browse the created dataset
streamlit run streamlit/browse_dataset.py -- --data-dir output/ExamplesStringsCriterion_10k/dataset

# Finetune model
python finetuning/run_clm.py configs/finetune/ExamplesStringsCriterion_10k.json
```