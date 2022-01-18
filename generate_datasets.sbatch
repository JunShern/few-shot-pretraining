#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --time=48:00:00
#SBATCH --mem=64GB

#SBATCH --job-name=generate_datasets

## This places the standard output and standard error into the same file, in this case slurm_<job_id>.out 
#SBATCH --output=/scratch/jc11431/slurm_logs/slurm_%j.out

## First we ensure a clean environment by purging the current one
module purge

## Load Anaconda
module load anaconda3/2020.07
source ~/.bashrc
conda activate alignment

## Just log environment stats for diagnostics
myquota
nvidia-smi
which python
wandb login

## Run experiment
cd $HOME/git/few-shot-pretraining
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t200k.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_t1M.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_t10M.yaml

# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_val_t10k.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_val_t10k.yaml

# time python finetune_with_dataset.py -d configs/dataset/ListPrefixV2Criterion_t10k.yaml -v configs/dataset/ListPrefixV2Criterion_val_t1k.yaml
# time python finetune_with_dataset.py -d configs/dataset/AllDocuments_t10k.yaml -v configs/dataset/AllDocuments_val_t1k.yaml
# time python finetune_with_dataset.py -d configs/dataset/QuestionAnswerStringsV2Criterion_t10k.yaml -v configs/dataset/QuestionAnswerStringsV2Criterion_val_t1k.yaml
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t10k.yaml -v configs/dataset/ExamplesStringsCriterion_val_t1k.yaml

# time python finetune_with_dataset.py -d configs/dataset/ColonListCriterion_t10k.yaml -v configs/dataset/ColonListCriterion_val_t1k.yaml
# time python finetune_with_dataset.py -d configs/dataset/ExamplesStringsV3Criterion_t10k.yaml -v configs/dataset/ExamplesStringsV3Criterion_val_t1k.yaml