#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:rtx8000:1
#SBATCH --time=5:00:00
#SBATCH --mem=64GB

#SBATCH --job-name=first_batch_train

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
python finetune_with_dataset.py -d configs/dataset/ExamplesStringsCriterion_t200.yaml -f configs/finetune/keeping_hits_constant/default_bs4_block512.json -m gpt2-large