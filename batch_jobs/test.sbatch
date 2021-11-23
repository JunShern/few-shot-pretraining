#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:01:00
#SBATCH --mem=2GB
#SBATCH --job-name=python-hello-world
#SBATCH --output=test.out

module purge
## Load Anaconda
module load anaconda3/2020.07
source ~/.bashrc
conda activate alignment

which python
python -c "print('jun says hello')"