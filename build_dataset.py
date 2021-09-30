import argparse
from pathlib import Path

from tqdm import tqdm

# from dataset.scavenger.writer import Writer
from common import utils
# import dataset.scavenger.criterion as cri
from dataset.scavenger.reader import C4Reader, DataSplit, PileReader

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build finetuning dataset with specified criteria')
    parser.add_argument("-c", "--config-file", help="Initial config file. Default: %(default)s")
    options = parser.parse_args()

    cfg = utils.load_config(options.config_file)

    print(cfg)
    

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Scavenger for text corpora")
#     parser.add_argument("--dataset", type=str, required=True,
#                         help="Name of dataset. One of [C4, Pile]")
#     parser.add_argument("--data-dir", type=str, default="./data",
#                         help="Root directory containing input text datasets. Default: %(default)s")
#     parser.add_argument("--output-dir", type=str, default="./output",
#                         help="Destination directory for saving output results. Default: %(default)s")
#     parser.add_argument("--max-documents", type=int, default=10000,
#                         help="Maximum no. of documents from the dataset to process. Default: %(default)s")
#     options = parser.parse_args()

    # criteria = [
    #     cri.AllDocuments(),
    #     # cri.DomainCriterion(valid_domains=["stackoverflow", "stackexchange", "quora", "arxiv", "reddit", "wikipedia"]),
    #     # cri.QuestionAnswerStringsCriterion(),
    #     cri.QuestionAnswerStringsV2Criterion(),
    #     cri.FullyStructuredCriterion(),
    #     # cri.ExamStringsCriterion(),
    #     cri.ExamStringsV2Criterion(),
    #     # cri.QuestionStringsCriterion(),
    #     cri.ExamplesStringsCriterion(),
    #     cri.ExamplesStringsV2Criterion(),
    #     # cri.NewlineOccurrenceCriterion(),
    #     # cri.ListPrefixCriterion(),
    #     cri.ListPrefixV2Criterion(),
    #     cri.ExamplesMinimalEmbedCriterion(),
    #     cri.ExamplesSynonymsEmbedCriterion(),
    #     cri.ExamplesDiverseEmbedCriterion(),
    #     ]

    # writer = Writer(options.output_dir, headers=[str(c) for c in criteria])
    # data_split = DataSplit.VAL # Prototype on the small subset
    # if options.dataset == "C4":
    #     reader = C4Reader(options.data_dir, data_split=data_split)
    # elif options.dataset == "Pile":
    #     reader = PileReader(options.data_dir, data_split=data_split)
    # else:
    #     print(f"Dataset {options.dataset} not supported!")
    #     exit()
    
    # for idx, doc in tqdm(enumerate(reader)):
    #     if options.max_documents is not None and idx >= options.max_documents:
    #         break

    #     results = {}
    #     for criterion in criteria:
    #         results[str(criterion)] = criterion.check(doc)
        
    #     doc_id = f"{idx}" # TODO: How can we make this a better identifier?
    #     writer.add(doc_id, results, text=doc.text)
    
    # print(f"Processed {idx + 1} documents.")
