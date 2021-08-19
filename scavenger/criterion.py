from abc import ABC, abstractmethod
from scavenger.document import Document

class Criterion(ABC):
    def __init__(self):
        return

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @abstractmethod
    def check(document: Document) -> bool:
        pass

class DomainCriterion(Criterion):
    def __init__(self, valid_domains):
        super().__init__()
        self._valid_domains = valid_domains

    def check(self, document: Document) -> bool:
        if document.source is None:
            return False
        for domain in self._valid_domains:
            if domain in document.source:
                return True
        return False

class QuestionAnswerStringsCriterion(Criterion):
    def __init__(
        self, 
        valid_strings = ["Q&A", "Q & A", "FAQ", "Frequently Asked Questions", "Q:", "Question:", "A:", "Answer:"]
        ):
        super().__init__()
        self._valid_strings = valid_strings

    def check(self, document: Document) -> bool:
        for qna_string in self._valid_strings:
            if qna_string in document.text:
                return True
        return False