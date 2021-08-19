from scavenger.checker import Checker
from scavenger.reader import PileReader
from scavenger.criterion import DomainCriterion, QuestionAnswerStringsCriterion
# writer = Writer()

checker = Checker()
for c in [
    DomainCriterion(valid_domains=["stackoverflow", "quora", "arxiv", "reddit", "wikipedia"]),
    QuestionAnswerStringsCriterion()
    ]:
    checker.add_criterion(c)

reader = PileReader("./data")
for idx, doc in enumerate(reader):
    any_passed, result = checker.check(doc)
    if any_passed:
        print("-" * 100)
        print(doc.text[:300])
        print("\n\n\n\n")
        print(result)
    # writer.add(doc_id, passing_criteria)

    if idx > 100:
        break