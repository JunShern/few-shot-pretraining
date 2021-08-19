from scavenger.criterion import Criterion
from scavenger.document import Document

class Checker:
    def __init__(self):
        self._criteria: list[Criterion] = []

    def add_criterion(self, criterion: Criterion):
        self._criteria.append(criterion)
    
    def check(self, document: Document) -> "tuple[bool, list[tuple[str, bool]]]":
        results: list[tuple[str, bool]] = []
        any_passed = False
        for criterion in self._criteria:
            passed = criterion.check(document)
            results.append((str(criterion), passed))
            if passed:
                any_passed = True
        return any_passed, results