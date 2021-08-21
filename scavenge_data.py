import argparse
import scavenger.criterion as cri
from scavenger.checker import Checker
from scavenger.reader import PileReader
from scavenger.writer import Writer
from tqdm import tqdm


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scavenger for text corpora")
    parser.add_argument("--data-dir", type=str, default="./data",
                        help="Root directory containing input text datasets Default: %(default)s")
    parser.add_argument("--output-file", type=str, default="./output/results.csv",
                        help="Destination filepath for saving output results. Default: %(default)s")
    parser.add_argument("--max-documents", type=int, default=1000,
                        help="Maximum no. of documents from the dataset to process. Default: %(default)s")
    options = parser.parse_args()

    checker = Checker()
    for c in [
        cri.AllDocuments(),
        cri.DomainCriterion(valid_domains=["stackoverflow", "quora", "arxiv", "reddit", "wikipedia"]),
        cri.QuestionAnswerStringsCriterion(),
        cri.FullyStructuredCriterion(),
        cri.ExamStringsCriterion(),
        cri.QuestionStringsCriterion(),
        cri.StringsMatchCriterion(["interview transcript", "transcript of our interview", "Interview"]),
        ]:
        checker.add_criterion(c)

    reader = PileReader(options.data_dir)
    writer = Writer(options.output_file, headers=checker.get_criteria())
    
    for idx, doc in tqdm(enumerate(reader)):
        if options.max_documents is not None and idx >= options.max_documents:
            break

        any_passed, result = checker.check(doc)
        
        doc_id = f"{reader.get_data_root()}_{idx}"
        preview_text = doc.text[:100].replace("\n", "")
        writer.add(doc_id, result, preview=preview_text)
    
    print(f"Processed {idx} documents.")