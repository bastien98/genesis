from abc import ABC, abstractmethod
from langchain_core.documents import Document

from file_api.core.domain.file_location import DocumentLocation, DirectoryLocation


class FileStoragePort(ABC):
    @abstractmethod
    def _calculate_raw_output_location(self, filename: str) -> DocumentLocation:
        pass

    @abstractmethod
    def calculate_clean_output_location(self, filename: str) -> DocumentLocation:
        pass

    @abstractmethod
    async def save_raw_content(self, content: bytes, filename: str) -> None:
        pass

    @abstractmethod
    async def save_clean_document(self, document: Document, filename: str) -> None:
        pass

    @abstractmethod
    async def read_documents(self, location: DirectoryLocation) -> list[Document]:
        pass
