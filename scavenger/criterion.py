import json
import re
import yaml
from abc import ABC, abstractmethod
from scavenger.document import Document

class Criterion(ABC):
    def __init__(self):
        return

    def __str__(self) -> str:
        return self.__class__.__name__.replace("Criterion", "")
    
    @abstractmethod
    def check(document: Document) -> bool:
        pass

class AllDocuments(Criterion):
    def __init__(self):
        super().__init__()
    
    def check(self, document: Document) -> bool:
        return True

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

class FullyStructuredCriterion(Criterion):
    def __init__(self):
        super().__init__()

    def check_json(self, text):
        try:
            _ = json.loads(text)
        except ValueError as e:
            return False
        return True

    def check_markdown(self, text):
        match = re.search("\[.+\]\(https*:\/\/\S+\)", text)
        return bool(match)

    def check_yaml(self, text):
        if type(yaml.safe_load(text)) == dict:
            return True
        return False

    def check(self, document: Document) -> bool:
        if self.check_json(document.text):
            return True
        elif self.check_markdown(document.text):
            return True
        # elif self.check_yaml(document.text):
        #     return True
        return False

class StringsMatchCriterion(Criterion):
    def __init__(self, valid_strings):
        super().__init__()
        self._valid_strings = valid_strings

    def check(self, document: Document) -> bool:
        for qna_string in self._valid_strings:
            if qna_string in document.text:
                return True
        return False

class QuestionAnswerStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        valid_strings = ["Q&A", "Q & A", "FAQ", "Frequently Asked Questions", "Q:", "Question:", "A:", "Answer:"]
        ):
        super().__init__(valid_strings)

class ExamStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        valid_strings = ["GRE", "SAT", "TOEFL", "A-levels", "IGCSE"]
        ):
        super().__init__(valid_strings)
        self._valid_strings = valid_strings

class QuestionStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        valid_strings = ["?\n", "? \n"]
        ):
        super().__init__(valid_strings)
        self._valid_strings = valid_strings