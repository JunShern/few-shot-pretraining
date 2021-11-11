#!/bin/bash

# wget -m -np -c -U "eye02" -w 2 -R "index.html*" "https://the-eye.eu/public/AI/pile/"
wget -m -np -c -U "eye02" -w 2 "https://the-eye.eu/public/AI/pile/val.jsonl.zst" --no-check-certificate