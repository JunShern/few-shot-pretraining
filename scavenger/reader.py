import datasets
import lm_dataformat as lmd
from datasets import load_dataset
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

class C4Reader(Reader):
    def __init__(self, _data_root):
        super().__init__(_data_root)
        dataset = datasets.load_dataset('c4', 'en', cache_dir=self._data_root)
        self._dataset = dataset['train']
        self._index = 0

    def __next__(self):
        doc = Document(
            text = self._dataset[self._index]['text'],
            corpus = "C4",
            source = self._dataset[self._index]['url'],
        )
        self._index += 1
        return doc