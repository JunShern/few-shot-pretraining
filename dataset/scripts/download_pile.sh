#!/bin/bash

mkdir ./base_datasets/pile
pushd ./base_datasets/pile
# wget -m -np -c -U "eye02" -w 2 -R "index.html*" "https://the-eye.eu/public/AI/pile/"
wget -m -np -c -U "eye02" -w 2 "https://the-eye.eu/public/AI/pile/val.jsonl.zst" --no-check-certificate
popd