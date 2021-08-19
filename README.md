# NLP Scavenger / Raccoon

## Getting the data

#### [The Pile](https://pile.eleuther.ai/)
Download data (Beware: 400+ GiB)
```bash
wget -m -np -c -U "eye02" -w 2 -R "index.html*" "https://the-eye.eu/public/AI/pile/"
```

```bash
# AWS DL machine environment
conda create --name scavenger --clone python3
conda activate scavenger

# From scratch
conda create --name scavenger python=3.8
conda activate scavenger
pip install -r requirements.txt
```

### C4
