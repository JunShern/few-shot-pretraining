import csv
from pathlib import Path

class Writer:
    def __init__(self, filepath: str, headers: list):
        # Output path
        self.filepath = filepath
        Path(self.filepath).parent.mkdir(parents=True, exist_ok=True)
        # File headers
        self.headers = ["doc_id"] + list(headers) + ["preview"]
        with open(self.filepath, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writeheader()
    
    def add(self, doc_id: str, results: dict, preview: str = ""):
        results["doc_id"] = doc_id
        results["preview"] = preview
        with open(self.filepath, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=self.headers)
            writer.writerow(results)