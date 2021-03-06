import csv
import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

import nltk
import yaml

from .document import Document
from .embeddings import Embed


@dataclass
class CriterionReport:
    criterion: str
    passed: bool
    reason: str
    trimmed_text: str = None

class Criterion(ABC):
    def __init__(self):
        return

    def __str__(self) -> str:
        return self.__class__.__name__.replace("Criterion", "")

    def _report(self, passed, reason = "Does not meet criterion.", trimmed_text = None):
        return CriterionReport(
            criterion = str(self), 
            passed = passed,
            reason = reason,
            trimmed_text = trimmed_text)

    @abstractmethod
    def check(self, document: Document) -> CriterionReport:
        pass

class NoDocuments(Criterion):
    def __init__(self):
        super().__init__()
    
    def check(self, document: Document) -> CriterionReport:
        return self._report(
            passed = False,
            reason = "No documents pass.")

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
        query_strings = [
            "Here are some examples",
            "Here is a list of",
        ]):
        super().__init__(query_strings)

class ExamplesStringsV2Criterion(StringsMatchCriterion):
    def __init__(
        self, 
        query_strings = [
            "Below are a few",
            "Below are some",
            "Examples include",
            "Here are a",
            "Here are some",
            "Here is a list of",
            "I have a list of",
            "A few examples of",
            "Some examples of",
            "There are a number of",
            "There are many",
            "There are quite a few",
            "These are some",
            "This includes",
        ]):
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
    def __init__(self, regex_query, multiline=True, ignore_case=False, min_hits=0, chars_before=0, chars_after=0):
        super().__init__()
        self._regex_query = regex_query
        self._min_hits = min_hits
        self.re_flags = 0
        if multiline:
            self.re_flags = self.re_flags | re.M
        if ignore_case:
            self.re_flags = self.re_flags | re.I
        self.chars_before = chars_before
        self.chars_after = chars_after

    def check(self, document: Document) -> CriterionReport:
        matches = re.compile(self._regex_query, flags = self.re_flags).finditer(document.text)
        groups = [(m.group(0), m.start(), m.end()) for m in matches]
        if len(groups) > self._min_hits:
            # Trimmed text is an optional field, set None by default
            trimmed_text = None
            if self.chars_before != 0 and self.chars_after != 0:
                trimmed_text = []
                for _, start_idx, end_idx in groups:
                    trimmed_text.append(document.text[start_idx - self.chars_before : end_idx + self.chars_after])
                trimmed_text = "\n\n".join(trimmed_text)
            return self._report(
                passed = True,
                reason = f"Text contains {groups}.",
                trimmed_text = trimmed_text,
                )
        return self._report(passed = False)

class QuestionAnswerStringsV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"\b(Q&A|Q & A|FAQ|Frequently Asked Questions|Q:|Question:|A:|Answer:)",
        multiline=True,
        ):
        super().__init__(regex_query, multiline=multiline)

class ExamStringsV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"\b(GRE|SAT|TOEFL|A Levels|IGCSE|JEE|IELTS)\b",
        multiline=True,
        ):
        super().__init__(regex_query, multiline=multiline)

class ListPrefixV2Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"^(\d|-|\*|\+)",
        multiline=True,
        min_hits=5,
        ):
        super().__init__(regex_query, multiline=multiline, min_hits=min_hits)

class ColonListCriterion(RegexCriterion):
    def __init__(self,
        regex_query = r"(list of|examples|include).{0,50}:\s*\n",
        multiline=True,
        ignore_case=True,
        min_hits=1,
        chars_before=200,
        chars_after=1000,
        ):
        super().__init__(regex_query, multiline=multiline, ignore_case=ignore_case, min_hits=min_hits, chars_before=chars_before, chars_after=chars_after)

class ExamplesStringsV3Criterion(RegexCriterion):
    def __init__(self,
        regex_query = r"(Here are some examples|Here is a list of)",
        multiline=True,
        ignore_case=True,
        min_hits=1,
        chars_before=200,
        chars_after=1000,
        ):
        super().__init__(regex_query, multiline=multiline, ignore_case=ignore_case, min_hits=min_hits, chars_before=chars_before, chars_after=chars_after)

class EmbedCriterion(Criterion):
    def __init__(self, query_strings, dist_threshold=0.2):
        super().__init__()
        self._dist_threshold = dist_threshold
        self._query_strings = query_strings
        self._em = Embed()
        self._mean_embed = self._em.get_mean_embedding(query_strings)
        nltk.download('punkt')

    def check(self, document: Document) -> CriterionReport:
        # Get all sentences from the document
        lines = document.text.split("\n")
        sentences = []
        for line in lines:
            if len(line) < 5:
                continue
            sentences += nltk.tokenize.sent_tokenize(line)
        # with open(f"/tmp/{self.__class__.__name__}.csv", "a") as f:
        #     writer = csv.writer(f)
        #     writer.writerow([sentence, dist])
        # Check the distance for each sentence
        hits = []
        for sentence in sentences:
            candidate_vec = self._em.get_embedding(sentence)
            dist = self._em.get_cosine_distance(self._mean_embed, candidate_vec)
            if dist <= self._dist_threshold and dist != 0:
                hits.append((sentence, dist))
        if len(hits) > 0:
            hits = [f"{hit} ({dist:.3f})" for hit, dist in hits]
            return self._report(
                passed = True,
                reason = f"Text contains {hits}.")
        return self._report(passed = False)

class ExamplesMinimalEmbedCriterion(EmbedCriterion):
    def __init__(self):
        query_strings = [
            'Here is a list of',
            'Here are some examples',
        ]
        super().__init__(query_strings)

class ExamplesSynonymsEmbedCriterion(EmbedCriterion):
    def __init__(self):
        query_strings = [
            'Here is a list of',
            'Here are some examples',
            "Some examples of",
            "There are a number of ways to",
            "Here are a list of",
            "I have a list of",
            "Here are a number of",
            "An example",
            "Examples include",
            "Another example",
            "Here are some of the",
            "These are some",
            "There are many ways to",
            "Here are some lists of",
            "For example",
            "This includes",
            "Here are some ways",
            "Here are some examples",
            "Here are a few other",
            "Below are a few",
            "There are quite a few ways to",
            "Here are a few ways to",
        ]
        super().__init__(query_strings)

class ExamplesDiverseEmbedCriterion(EmbedCriterion):
    def __init__(self):
        query_strings = [
            'Here is a list of',
            'Here are some examples',
            'For example',
            'Here are some different',
            'Examples include',
            "Here are some examples of",
            "I have a list of",
            "These are some different ways to",
            "There are many, such as",
            "These are my favorite news articles",
            "The following are the best restaurants in",
            "Top 10 places to visit",
            "Some of the best singers of 2020",
            "I like all kinds of dinosaurs, including",
            "The greatest bands in the world",
            "Top spots for taking pictures",
            "You may encounter any of the following",
        ]
        super().__init__(query_strings)
