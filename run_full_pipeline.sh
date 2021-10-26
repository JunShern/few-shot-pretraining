#!/bin/bash

OUTPUT_BASE=output/ExamplesStringsCriterion_10k
DATASET_CONFIG=configs/dataset/ExamplesStringsCriterion_10k.yaml
FINETUNE_CONFIG=configs/finetune/ExamplesStringsCriterion_10k.json
# TODO: How can we ensure that the out dir in the config files is consistent with OUTPUT_BASE?

# Copy configs into output dir
mkdir -p $OUTPUT_BASE/configs/
cp $DATASET_CONFIG $OUTPUT_BASE/configs/
cp $FINETUNE_CONFIG $OUTPUT_BASE/configs/

# Build a small test dataset:
echo "Building dataset with config $DATASET_CONFIG"
python dataset/build_dataset.py -c $DATASET_CONFIG

# Finetune model
echo "Finetuning model with config $FINETUNE_CONFIG"
python finetuning/run_clm.py $FINETUNE_CONFIG
