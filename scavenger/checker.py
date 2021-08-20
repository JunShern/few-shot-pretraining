from scavenger.criterion import Criterion
from scavenger.document import Document

class Checker:
    def __init__(self):
        self._criteria: list[Criterion] = []

    def add_criterion(self, criterion: Criterion):
        self._criteria.append(criterion)
    
    def check(self, document: Document) -> "tuple[bool, dict[str: bool]]":
        results: dict[str: bool] = {}
        any_passed = False
        for criterion in self._criteria:
            passed = criterion.check(document)
            results[str(criterion)] = passed
            if passed:
                any_passed = True
        return any_passed, results
    
    def get_criteria(self) -> "list[str]":
        return [str(c) for c in self._criteria]