import argparse

from tqdm import tqdm

import dataset.curator.criterion as cri
from common import utils
from dataset.curator.reader import C4Reader, PileReader
from dataset.curator.writer import Writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build finetuning dataset with specified criteria')
    parser.add_argument("-c", "--config-file", required=True, help="Config file")
    options = parser.parse_args()

    # Load params
    cfg = utils.load_config(options.config_file)

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

    # Process datasets
    for base_dataset in cfg.base_datasets:
        print(f"Processing {base_dataset} dataset...")
        writer = Writer(cfg.output_dir, headers=[str(c) for c in criteria])

        # Instantiate readers
        if base_dataset == "C4":
            reader = C4Reader(cfg.base_datasets_dir, data_split=cfg.data_split)
        elif base_dataset == "Pile":
            reader = PileReader(cfg.base_datasets_dir, data_split=cfg.data_split)
        else:
            print(f"Dataset {base_dataset} not supported!")
            exit()
        
        # Check each document in dataset
        for idx, doc in tqdm(enumerate(reader), total=len(reader)):
            results = {}
            for criterion in criteria:
                results[str(criterion)] = criterion.check(doc)
            
            doc_id = f"{base_dataset}_{cfg.data_split}_{idx}"
            writer.add_entry(doc_id, results, text=doc.text)

            if cfg.max_documents is not None and idx + 1 >= cfg.max_documents:
                break
    
    print(f"Processed {idx + 1} documents.")
    print(f"Outputs saved to {cfg.output_dir}.")
