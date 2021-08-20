import lm_dataformat as lmd
from abc import ABC, abstractmethod
from scavenger.document import Document
from pathlib import Path

class Reader(ABC):
    def __init__(self, _data_root: str):
        self._data_root = Path(_data_root)
    
    def get_data_root(self):
        return str(self._data_root)
    
    def __iter__(self):
        return self
    
    @abstractmethod
    def __next__(self):
        pass

class PileReader(Reader):
    def __init__(self, _data_root):
        super().__init__(_data_root)
        self._reader = lmd.Reader(str(self._data_root / "the-eye.eu/public/AI/pile/val.jsonl.zst"))
        self._stream = self._reader.stream_data()

    def __next__(self):
        doc = Document(
            text = next(self._stream),
            corpus = "The Pile"
        )
        return doc