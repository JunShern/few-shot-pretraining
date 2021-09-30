# NLP Scavenger / Raccoon

```bash
conda create --name nlp python=3.8
conda activate nlp
pip install -r requirements.txt
```

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
python scavenge_data.py --dataset Pile --data-dir /data/pile --output-dir ./output/pile/
python scavenge_data.py --dataset C4 --data-dir /data/c4 --output-dir ./output/c4/
```

## Visualizing the output
visualize.ipynb

streamlit run browse_results.py -- --data-dir ./output