#!/bin/bash

# On Remote
rm -r output
rm output.tar
time python scavenge_data.py --dataset Pile --data-dir /data/pile --output-dir ./output/pile/
time python scavenge_data.py --dataset C4 --data-dir /data/c4 --output-dir ./output/c4/
# time zip -r output.zip output
time tar -cf output.tar output/ # Without compression, much faster

# # On Local
# scp -i ~/.ssh/aws-dl.pem ubuntu@$REMOTE_ADDRESS:~/git/few-shot-pretraining/output.tar .
# tar -xf output.tar