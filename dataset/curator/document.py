from dataclasses import dataclass


@dataclass
class Document:
    text: str
    source: str = None
    corpus: str = None
