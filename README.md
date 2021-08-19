# Scavenger NLP Raccoon

# Getting the data
## [The Pile](https://pile.eleuther.ai/)
Download data (Beware: 400+ GiB)
```bash
wget -m -np -c -U "eye02" -w 2 -R "index.html*" "https://the-eye.eu/public/AI/pile/"
```

```bash
conda create --name pile --clone python3 # AWS DL machine environment
conda activate pile
pip install -r requirements.txt
```

## C4


Scripts

get_data.sh

reader.py
c4_reader.py
pile_reader.py

criterion.py
domain_criterion
regex_structure_criterion
full_structure_criterion

writer = Writer()

for c in [DomainCriterion, RegexStructureCriterion]:
    checker.add_criterion(c)

for doc in reader:
    passing_critera = checker.check(doc)
    writer.add(doc_id, passing_criteria)