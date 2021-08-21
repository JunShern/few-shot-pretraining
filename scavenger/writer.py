import csv
from pathlib import Path

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
    
    def add(self, doc_id: str, results: dict, text: str):
        results["doc_id"] = doc_id
        results["preview"] = text[:100].replace("\n", "")
        with open(self.outfile_path, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(results)
        
        # Save out full text if it passes any (interesting) criteria
        any_criteria_passed = any([
            val for key, val in results.items() 
            if type(val) == bool and key != "AllDocuments"
            ])
        if any_criteria_passed:
            text_path = (self.outdir_path / doc_id).with_suffix(".txt")
            with open(str(text_path), "w") as f:
                f.write(text)