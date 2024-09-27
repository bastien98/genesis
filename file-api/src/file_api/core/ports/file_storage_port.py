from abc import ABC, abstractmethod
from langchain_core.documents import Document

from file_api.core.domain.file_location import FileLocation


class FileStoragePort(ABC):
    @abstractmethod
    def _calculate_raw_output_location(self, filename: str) -> FileLocation:
        pass

    @abstractmethod
    def calculate_clean_output_location(self, filename: str) -> FileLocation:
        pass

    @abstractmethod
    async def save_raw_content(self, content: bytes, filename: str) -> None:
        pass

    @abstractmethod
    async def save_clean_document(self, document: Document, filename: str) -> None:
        pass
