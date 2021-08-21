import argparse
import scavenger.criterion as cri
from scavenger.checker import Checker
from scavenger.reader import C4Reader, PileReader
from scavenger.writer import Writer
from tqdm import tqdm


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scavenger for text corpora")
    parser.add_argument("--dataset", type=str, required=True,
                        help="Name of dataset. One of [C4, Pile]")
    parser.add_argument("--data-dir", type=str, default="./data",
                        help="Root directory containing input text datasets. Default: %(default)s")
    parser.add_argument("--output-dir", type=str, default="./output",
                        help="Destination directory for saving output results. Default: %(default)s")
    parser.add_argument("--max-documents", type=int, default=100000,
                        help="Maximum no. of documents from the dataset to process. Default: %(default)s")
    options = parser.parse_args()

    checker = Checker()
    for c in [
        cri.AllDocuments(),
        cri.DomainCriterion(valid_domains=["stackoverflow", "stackexchange", "quora", "arxiv", "reddit", "wikipedia"]),
        cri.QuestionAnswerStringsCriterion(),
        cri.FullyStructuredCriterion(),
        cri.ExamStringsCriterion(),
        cri.QuestionStringsCriterion(),
        cri.StringsMatchCriterion(["interview transcript", "transcript of our interview", "Interview"]),
        ]:
        checker.add_criterion(c)

    writer = Writer(options.output_dir, headers=checker.get_criteria())
    if options.dataset == "C4":
        reader = C4Reader(options.data_dir)
    elif options.dataset == "Pile":
        reader = PileReader(options.data_dir)
    else:
        print(f"Dataset {options.dataset} not supported!")
        exit()
    
    for idx, doc in tqdm(enumerate(reader)):
        if options.max_documents is not None and idx >= options.max_documents:
            break

        any_passed, result = checker.check(doc)
        
        doc_id = f"{idx}" # TODO: How can we make this a better identifier?
        writer.add(doc_id, result, text=doc.text)
    
    print(f"Processed {idx} documents.")