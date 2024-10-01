from abc import ABC, abstractmethod
from langchain_core.documents import Document
from file_api.core.domain.file_location import DocumentLocation, DirectoryLocation
from rank_bm25 import BM25Okapi


class FileStoragePort(ABC):
    @abstractmethod
    def get_kb_location(self, kb_id: str) -> DirectoryLocation:
        pass

    @abstractmethod
    def get_kb_files_location(self, kb_id: str) -> DirectoryLocation:
        pass

    @abstractmethod
    def get_BM25_index_location(self, kb_id: str) -> DocumentLocation:
        pass

    @abstractmethod
    def get_markdown_location(self, filename: str, kb_id: str) -> DocumentLocation:
        pass

    @abstractmethod
    def get_raw_location(self, filename: str, kb_id: str) -> DocumentLocation:
        pass

    @abstractmethod
    def get_text_location(self, filename: str, kb_id: str) -> DocumentLocation:
        pass

    @abstractmethod
    def save_BM25_index(self, index: BM25Okapi, kb_id: str) -> None:
        pass

    @abstractmethod
    def save_markdown_document(self, document: Document, filename: str, kb_id: str) -> None:
        pass

    @abstractmethod
    def save_raw_document(self, content: bytes, filename: str, kb_id: str) -> None:
        pass

    @abstractmethod
    def save_text_document(self, documents: Document, filename: str, kb_id: str) -> None:
        pass

    @abstractmethod
    def read_BM25_index(self, location: DocumentLocation) -> BM25Okapi:
        pass

    # @abstractmethod
    # def create_BM25_index(self, kb_id: str) -> None:
    #     pass

