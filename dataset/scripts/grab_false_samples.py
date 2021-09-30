import json
import random
from pathlib import Path

indir = Path("./output_10k/")
outdir = Path("./embeddings/ExamplesStrings/false")

filepaths = list(indir.glob("**/*.txt"))
random.seed(0)
random.shuffle(filepaths)
filepaths = filepaths[:100]
for idx, filepath in enumerate(filepaths):
    with open(filepath, "r") as f:
        doc = json.load(f)
        for cri in doc["criteria"]:
            if cri["criterion"] == "ExamplesStrings" and cri["passed"] == False:
                outpath = outdir / filepath.parent.name / filepath.name
                print("Gonna save to ", outpath)
                with open(outpath, "w") as f:
                    f.write(doc["text"])
