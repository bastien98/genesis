from abc import ABC, abstractmethod

from langchain_core.documents import Document


class FileStoragePort(ABC):
    @abstractmethod
    async def save_raw_document(self, file: bytes, file_name: str) -> str:
        pass
