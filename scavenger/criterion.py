import json
import re
import yaml
from abc import ABC, abstractmethod
from dataclasses import dataclass
from scavenger.document import Document

@dataclass
class CriterionReport:
    criterion: str
    passed: bool
    reason: str

class Criterion(ABC):
    def __init__(self):
        return

    def __str__(self) -> str:
        return self.__class__.__name__.replace("Criterion", "")

    def _report(self, passed, reason = "Does not meet criterion."):
        return CriterionReport(
            criterion = str(self), 
            passed = passed,
            reason = reason)

    @abstractmethod
    def check(self, document: Document) -> CriterionReport:
        pass

class AllDocuments(Criterion):
    def __init__(self):
        super().__init__()
    
    def check(self, document: Document) -> CriterionReport:
        return self._report(
            passed = True,
            reason = "All documents pass.")

class DomainCriterion(Criterion):
    def __init__(self, valid_domains):
        super().__init__()
        self._valid_domains = valid_domains

    def check(self, document: Document) -> CriterionReport:
        if document.source is None:
            return self._report(
                passed = False,
                reason = "Document source unavailable.")
        for domain in self._valid_domains:
            if domain in document.source:
                return self._report(
                    passed = True,
                    reason = f"{document.source} contains {domain}")
        return self._report(passed = False)

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

    def check(self, document: Document) -> CriterionReport:
        if self.check_json(document.text):
            return self._report(
                passed = True,
                reason = "Text is JSON.")
        elif self.check_markdown(document.text):
            return self._report(
                passed = True,
                reason = "Text contains Markdown.")
        # TODO: YAML safe_load is not in fact safe
        # elif self.check_yaml(document.text):
        #     return self._report(
        #         passed = True,
        #         reason = "Text is YAML.")
        return self._report(passed = False)

class StringsMatchCriterion(Criterion):
    def __init__(self, query_strings):
        super().__init__()
        self._query_strings = query_strings

    def check(self, document: Document) -> CriterionReport:
        for query_string in self._query_strings:
            if query_string in document.text:
                return self._report(
                    passed = True,
                    reason = f"Text contains {query_string}.")
        return self._report(passed = False)

class QuestionAnswerStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = ["Q&A", "Q & A", "FAQ", "Frequently Asked Questions", "Q:", "Question:", "A:", "Answer:"]
        ):
        super().__init__(query_strings)

class ExamStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = ["GRE", "SAT", "TOEFL", "A-levels", "IGCSE"]
        ):
        super().__init__(query_strings)

class QuestionStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = ["?\n", "? \n"]
        ):
        super().__init__(query_strings)

class InterviewStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = ["interview transcript", "transcript of our interview", "Interview"]
        ):
        super().__init__(query_strings)

class ExamplesStringsCriterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = ["Here are some examples", "Here is a list of"]
        ):
        super().__init__(query_strings)

class NewlineOccurrenceCriterion(Criterion):
    def __init__(self, newlines_per_chars_thresh=1/100):
        super().__init__()
        self.newlines_per_chars_thresh = newlines_per_chars_thresh

    def check(self, document: Document) -> CriterionReport:
        if len(document.text) == 0:
            return self._report(
                passed = False,
                reason = "Text is empty.")
        newlines = document.text.count("\n")
        chars = len(document.text)
        newlines_per_chars = newlines / chars
        return self._report(
            passed = newlines_per_chars >= self.newlines_per_chars_thresh,
            reason = f"Score: {newlines_per_chars:.3f} | "\
                f"Threshold: {self.newlines_per_chars_thresh:.3f} | "\
                f"Newlines: {newlines} | Chars: {chars}")

class ListPrefixCriterion(Criterion):
    def __init__(self, min_prefixes=5):
        super().__init__()
        self.min_prefixes = min_prefixes
        self.prefixes = ["-", "*", "+", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    def check(self, document: Document) -> CriterionReport:
        first_chars = [line.strip() for line in document.text.split("\n") if len(line.strip()) > 0]
        matches = 0
        for first_char in first_chars:
            if first_char in self.prefixes:
                matches += 1
        return self._report(
            passed = matches >= self.min_prefixes,
            reason = f"Found {matches} list prefixes. (Min: {self.min_prefixes})")

class RegexCriterion(Criterion):
    def __init__(self, regex_query, multiline=True, min_hits=0):
        super().__init__()
        self._regex_query = regex_query
        self._multiline = multiline
        self._min_hits = min_hits

    def check(self, document: Document) -> CriterionReport:
        re_flags = (re.M if self._multiline else 0)
        hits = re.compile(self._regex_query, re_flags).findall(document.text)
        if len(hits) > self._min_hits:
            return self._report(
                passed = True,
                reason = f"Text contains {hits}.")
        return self._report(passed = False)

class QuestionAnswerStringsV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"\b(Q&A|Q & A|FAQ|Frequently Asked Questions|Q:|Question:|A:|Answer:)",
        multiline=True,
        ):
        super().__init__(regex_query, multiline)

class ExamStringsV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"\b(GRE|SAT|TOEFL|A Levels|IGCSE|JEE|IELTS)\b",
        multiline=True,
        ):
        super().__init__(regex_query, multiline)

class ListPrefixV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"^(\d|-|\*|\+)",
        multiline=True,
        min_hits=5,
        ):
        super().__init__(regex_query, multiline)
