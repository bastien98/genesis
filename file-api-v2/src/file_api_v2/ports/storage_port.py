from abc import ABC, abstractmethod

from fastapi import UploadFile
from rank_bm25 import BM25Okapi


class FileStoragePort(ABC):

    @abstractmethod
    def save_raw_file(self, document: bytes, location: str) -> None:
        pass

    @abstractmethod
    def save_md_chunks(self, chunks: list[str], location: str) -> None:
        pass

    @abstractmethod
    def save_text_chunks(self, chunks: list[str], location: str) -> None:
        pass

    @abstractmethod
    def read_text_chunks(self, location: str) -> list[str]:
        pass

    @abstractmethod
    def save_BM25_index(self, bm25_index: BM25Okapi, location: str) -> None:
        pass

    @abstractmethod
    def read_BM25_index(self, location: str) -> BM25Okapi:
        pass



