import os
from abc import abstractmethod
from pathlib import Path


class AbstractDocumentManager:
    @abstractmethod
    def get_kb_location(self, kb_name: str) -> Path:
        pass

    @abstractmethod
    def get_raw_pdf_path(self, username: str, kb_name: str, doc_name: str) -> Path:
        pass

    @abstractmethod
    def get_chunked_pdf_path(self, username: str, kb_name, doc_name) -> Path:
        pass

    @abstractmethod
    def get_bm25_index_path(self, username: str, kb_name) -> Path:
        pass


class LocalFileSystemDocumentManager(AbstractDocumentManager):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path("../../../data/processed")).resolve()

    def get_kb_location(self, kb_name: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / kb_name).resolve()
        return kb_location

    def get_raw_pdf_path(self, username: str, kb_name: str, doc_name: str) -> Path:
        raw_location = (self.get_kb_location(kb_name) / "raw" / "pdf" / doc_name).resolve()
        return raw_location

    def get_chunked_pdf_path(self, username: str, kb_name: str, doc_name: str) -> Path:
        chunks_location = (self.get_kb_location(kb_name) / "chunked" / "pdf" / doc_name).resolve()
        return chunks_location

    def get_bm25_index_path(self, user_id: int, kb_id) -> Path:
        pass
