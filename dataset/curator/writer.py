import csv
import json
from dataclasses import asdict
from pathlib import Path

from .criterion import CriterionReport


class Writer:
    """
    Writes out a json file containing the document if it passes any criteria,
    along with the report for that document.
    Additionally creates a csv file summary.csv which stores a registry of all 
    the documents we process and pass/fail records of each criteria checked.
    """
    def __init__(self, output_dir: str, headers: list):
        # Output path
        self.outdir_path = Path(output_dir)
        self.outdata_path = self.outdir_path / "data"
        self.outdata_path.mkdir(parents=True, exist_ok=True)
        self.summary_path = self.outdir_path / "summary.csv"
        # File headers
        self.headers = ["doc_id"] + list(headers) + ["preview"]
        with open(self.summary_path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
    
    def add_entry(self, doc_id: str, results: "dict[str: CriterionReport]", text: str):
        # Append a row for this entry to summary.csv
        with open(self.summary_path, 'a') as f:
            row = {name: report.passed for name, report in results.items()}
            row["doc_id"] = doc_id
            row["preview"] = text[:100].replace("\n", "")
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(row)
        
        # Save out full text if it passes any criteria
        any_criteria_passed = any([report.passed for key, report in results.items()])
        if any_criteria_passed:
            # Save data file
            meta_path = (self.outdata_path / doc_id).with_suffix(".json")
            with open(str(meta_path), "w") as f:
                out_dict = {
                    "doc_id": doc_id,
                    "text": text,
                    "criteria": {}
                }
                for criterion_name, report in results.items():
                    out_dict['criteria'][criterion_name] = asdict(report)
                json.dump(out_dict, f, indent=4, sort_keys=True)