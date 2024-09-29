from abc import ABC, abstractmethod
from langchain_core.documents import Document
from file_api.core.domain.file_location import DocumentLocation, DirectoryLocation
from rank_bm25 import BM25Okapi


class FileStoragePort(ABC):
    @abstractmethod
    def _get_raw_output_location(self, filename: str, kb_id: str) -> DocumentLocation:
        pass

    @abstractmethod
    def get_clean_output_location(self, filename: str) -> DocumentLocation:
        pass

    @abstractmethod
    async def save_raw_content(self, content: bytes, filename: str, kb_id: str) -> None:
        pass

    @abstractmethod
    async def save_clean_document(self, document: Document, filename: str) -> None:
        pass

    @abstractmethod
    async def read_directory(self, location: DirectoryLocation) -> list[Document]:
        pass

    @abstractmethod
    async def save_BM25_index(self, index: BM25Okapi, filename: str) -> None:
        pass
