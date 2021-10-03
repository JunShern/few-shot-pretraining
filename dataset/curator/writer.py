import csv
import json
from dataclasses import asdict
from pathlib import Path

from .criterion import CriterionReport


class Writer:
    def __init__(self, output_dir: str, headers: list):
        # Output path
        self.outdir_path = Path(output_dir)
        self.outdir_path.mkdir(parents=True, exist_ok=True)
        self.outfile_path = self.outdir_path / "table.csv"
        # File headers
        self.headers = ["doc_id"] + list(headers) + ["preview"]
        with open(self.outfile_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
    
    def add_entry(self, doc_id: str, results: "dict[str: CriterionReport]", text: str):
        with open(self.outfile_path, 'a') as f:
            row = {name: report.passed for name, report in results.items()}
            row["doc_id"] = doc_id
            row["preview"] = text[:100].replace("\n", "")
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(row)
        
        # Save out full text if it passes any (interesting) criteria
        any_criteria_passed = any([
            report.passed for key, report in results.items() 
            if key != "AllDocuments"
            ])
        if any_criteria_passed:
            text_path = (self.outdir_path / doc_id).with_suffix(".txt")
            with open(str(text_path), "w") as f:
                json.dump({
                    "doc_id": doc_id,
                    "text": text,
                    "criteria": [asdict(report) for criterion_name, report in results.items()],
                }, f, indent=4, sort_keys=True)
