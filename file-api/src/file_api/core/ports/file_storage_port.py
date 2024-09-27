from abc import ABC, abstractmethod
from langchain_core.documents import Document
from file_api.core.domain.file_location import FileLocation


class FileStoragePort(ABC):
    @abstractmethod
    async def save_raw_content(self, content: bytes, filename: str) -> FileLocation:
        pass

    @abstractmethod
    async def save_clean_document(self, document: Document, file_location: FileLocation) -> FileLocation:
        pass
