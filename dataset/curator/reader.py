from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import datasets
import lm_dataformat as lmd

from .document import Document


class Reader(ABC):
    def __init__(self, data_root: str, data_split: str):
        self._data_root = Path(data_root)
        self._data_split = data_split
    
    def get_data_root(self):
        return str(self._data_root)
    
    def __iter__(self):
        return self
    
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def __len__(self):
        pass

class PileReader(Reader):
    def __init__(self, data_root: str, data_split="validation"):
        super().__init__(data_root, data_split)
        self._reset()
    
    def _reset(self):
        if self._data_split == "validation":
            self._reader = lmd.Reader(str(self._data_root / "pile/the-eye.eu/public/AI/pile/val.jsonl.zst"))
        elif self._data_split == "test":
            self._reader = lmd.Reader(str(self._data_root / "pile/the-eye.eu/public/AI/pile/test.jsonl.zst"))
        elif self._data_split == "train":
            raise NotImplementedError
        self._stream = self._reader.stream_data()

    def __next__(self):
        doc = Document(
            text = next(self._stream),
            corpus = "The Pile"
        )
        return doc

    def __len__(self):
        # TODO: DO BETTER!
        length = sum(1 for _ in self)
        self._reset() # Iterator has been exhausted
        return length

class C4Reader(Reader):
    def __init__(self, data_root: str, data_split="validation"):
        super().__init__(data_root, data_split)
        self._dataset = datasets.load_dataset('c4', 'en', cache_dir=self._data_root / "c4", split=data_split)
        self._index = 0
        self._length = len(self._dataset)

    def __next__(self):
        if self._index >= self._length:
            raise StopIteration
        doc = Document(
            text = self._dataset[self._index]['text'],
            corpus = "C4",
            source = self._dataset[self._index]['url'],
        )
        self._index += 1
        return doc

    def __len__(self):
        return self._length
