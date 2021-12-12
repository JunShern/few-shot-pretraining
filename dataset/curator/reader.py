from abc import ABC, abstractmethod
from enum import Enum
import time
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
        print(f"Loaded Pile:{data_split} with {len(self)} documents.")
    
    def _reset(self):
        self._readers = []
        self._reader_idx = 0
        if self._data_split == "validation":
            self._readers = [lmd.Reader(str(self._data_root / "pile/the-eye.eu/public/AI/pile/val.jsonl.zst"))]
        elif self._data_split == "test":
            self._readers = [lmd.Reader(str(self._data_root / "pile/the-eye.eu/public/AI/pile/test.jsonl.zst"))]
        elif self._data_split == "train":
            train_dir = self._data_root / "pile/the-eye.eu/public/AI/pile/train"
            for data_file in train_dir.glob("*.jsonl.zst"):
                self._readers.append(lmd.Reader(str(data_file)))
        assert len(self._readers) > 0
        self._stream = self._readers[self._reader_idx].stream_data()
        self._reader_idx += 1

    def __next__(self):
        text = next(self._stream)
        if text is None:
            if self._reader_idx < len(self._readers):
                self._stream = self._readers[self._reader_idx].stream_data()
                self._reader_idx += 1
            else:
                return None
        doc = Document(
            text = next(self._stream),
            corpus = "The Pile"
        )
        return doc

    def __len__(self):
        # TODO: DO BETTER!
        # length = sum(1 for _ in self)
        # self._reset() # Iterator has been exhausted
        # return length
        if self._data_split == "validation":
            return 214670
        if self._data_split == "test":
            return 214670
        if self._data_split == "train":
            return 210573810 # TODO: This is just an estimate using len(one .zst file) * 30; get the exact number!

class C4Reader(Reader):
    def __init__(self, data_root: str, data_split="validation"):
        super().__init__(data_root, data_split)
        start_time = time.time()
        self._dataset = datasets.load_dataset('c4', 'en', cache_dir=self._data_root / "c4", split=data_split)
        print(f"datasets.load_dataset took {time.time() - start_time} seconds")
        self._index = 0
        self._length = len(self._dataset)
        print(f"Loaded C4:{data_split} with {self._length} documents.")

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
