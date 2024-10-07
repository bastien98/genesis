from abc import ABC, abstractmethod

from fastapi import UploadFile


class StoragePort(ABC):

    @abstractmethod
    def saveRAW(self, document: bytes, location: str) -> None:
        pass

    @abstractmethod
    def save_md_chunks(self, chunks: list[str], location: str) -> None:
        pass

    @abstractmethod
    def save_text_chunks(self, chunks: list[str], location: str) -> None:
        pass

