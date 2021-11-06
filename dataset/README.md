## Getting the data
Download data (Need at least 2TB)

### [The Pile](https://pile.eleuther.ai/)
```bash
cd /data/pile
wget -m -np -c -U "eye02" -w 2 -R "index.html*" "https://the-eye.eu/public/AI/pile/"
```

### C4
```
python scripts/download_c4.py
```

## Processing the data
```bash
python build_dataset.py -c configs/dataset/ExamplesStringsCriterion_10k.yaml
```