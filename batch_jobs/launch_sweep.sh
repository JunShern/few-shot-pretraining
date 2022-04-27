#!/bin/bash
set -x

# Initialize sweep
SWEEP_CAPTURE=$(wandb sweep -p alignment_pretraining sweep.yaml 2>&1) # Initialize sweep and capture the terminal output
SWEEP_ID=$(echo $SWEEP_CAPTURE | awk '{print $NF}') # Grab the ID from the last line of the output
echo "Created sweep: $SWEEP_ID"

# Run jobs
echo "Launching workers for the sweep."
sbatch sweep.sbatch $SWEEP_ID