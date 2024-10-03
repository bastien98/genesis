import os
from abc import abstractmethod
from pathlib import Path


class AbstractDocumentManager:
    @abstractmethod
    def get_raw_pdf_path(self, user_id: str, kb_id, doc_id) -> Path:
        pass

    @abstractmethod
    def get_chunked_pdf_path(self, user_id: str, kb_id, doc_id, chunk_id) -> Path:
        pass

    @abstractmethod
    def get_bm25_index_path(self, user_id: str, kb_id) -> Path:
        pass


class LocalFileSystemDocumentManager(AbstractDocumentManager):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path("../../../data/processed")).resolve()

    def get_kb_location(self, kb_id: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / kb_id).resolve()
        return kb_location

    def get_raw_pdf_path(self, user_id: str, kb_id: str, doc_id: str) -> Path:
        raw_location = (self.get_kb_location(kb_id) / "raw" / "pdf" / doc_id).resolve()
        return raw_location

    def get_chunked_pdf_path(self, user_id: str, kb_id: str, doc_id: str, chunk_id) -> Path:
        chunks_location = (self.get_kb_location(kb_id) / "chunked" / "pdf" / doc_id).resolve()
        return chunks_location

    def get_bm25_index_path(self, user_id: str, kb_id) -> Path:
        pass
