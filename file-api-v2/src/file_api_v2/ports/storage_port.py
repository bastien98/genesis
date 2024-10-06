from abc import ABC, abstractmethod

from fastapi import UploadFile


class StoragePort(ABC):

    @abstractmethod
    def saveRAW(self, document: bytes, location: str) -> None:
        pass

