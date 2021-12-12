import argparse
import itertools
from pathlib import Path

from tqdm import tqdm

import dataset.curator.criterion as cri
from common import utils
from dataset.curator.reader import C4Reader, PileReader
from dataset.curator.writer import Writer


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis (https://docs.python.org/3/library/itertools.html)
    pending = len(iterables)
    nexts = itertools.cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = itertools.cycle(itertools.islice(nexts, pending))

def main(cfg):
    output_dir = Path(cfg.output_dir) / cfg.unique_name
    if output_dir.exists():
        print(f"{output_dir} already exists. Skipping dataset generation.")
        return

    # Create criteria for curation
    criteria = []
    for criterion_str in cfg.criteria:
        try:
            # Instantiate the right criterion class from string
            criterion = getattr(cri, criterion_str)()
            criteria.append(criterion)
        except AttributeError:
            print(f"Unable to find class {criterion_str} in module criterion")
            exit()
    print(f"Using criteria: {[str(c) for c in criteria]}")

    # Instantiate readers
    readers = []
    for base_dataset in cfg.base_datasets:
        if base_dataset == "C4":
            reader = C4Reader(cfg.base_datasets_dir, data_split=cfg.data_split)
        elif base_dataset == "Pile":
            reader = PileReader(cfg.base_datasets_dir, data_split=cfg.data_split)
        else:
            print(f"Dataset {base_dataset} not supported!")
            exit()
        readers.append(reader)
    multireader = roundrobin(*readers)
    
    # Process datasets
    num_hits = 0
    writer = Writer(output_dir, headers=[str(c) for c in criteria])
    # Check each document in dataset
    for idx, doc in tqdm(enumerate(multireader), total=sum([len(r) for r in readers])):
        results = {}
        found_hit = False
        for criterion in criteria:
            criterion_report = criterion.check(doc)
            results[str(criterion)] = criterion_report
            if criterion_report.passed:
                found_hit = True
        if found_hit:
            num_hits += 1
        
        doc_id = f"{doc.corpus}_{cfg.data_split}_{idx}"
        writer.add_entry(doc_id, results, text=doc.text)

        if "max_documents" in cfg and idx + 1 >= cfg.max_documents:
            break
        if "target_hits" in cfg and num_hits >= cfg.target_hits:
            break
    
    print(f"Processed {idx + 1} documents with {num_hits} hits.")
    print(f"Outputs saved to {output_dir}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build finetuning dataset with specified criteria')
    parser.add_argument("-c", "--config-file", required=True, help="Config file")
    options = parser.parse_args()

    # Load params
    cfg = utils.load_config(options.config_file)

    main(cfg)
