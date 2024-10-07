import os
from abc import abstractmethod
from pathlib import Path
from file_api_v2.ports.storage_port import StoragePort


class AbstractDocumentManager:
    @abstractmethod
    def saveRAW(self, document: bytes, doc_name: str, username: str, kb_name: str) -> str:
        pass

    @abstractmethod
    def save_md_chunks(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        pass

    @abstractmethod
    def save_text_chunks(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        pass


class DocumentManager(AbstractDocumentManager):

    def __init__(self, storage_adapter: StoragePort):
        self.storage_adapter = storage_adapter

    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path("../../../data/processed")).resolve()

    def _get_user_location(self, username: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / username).resolve()
        return kb_location

    def _get_kb_location(self, username:str, kb_name: str) -> Path:
        kb_location = self._get_user_location(username) / Path(kb_name)
        return kb_location

    def saveRAW(self, document: bytes, doc_name: str, username: str, kb_name: str) -> str:
        raw_location = str((self._get_kb_location(username, kb_name) / "raw" / "pdf" / doc_name).resolve())
        self.storage_adapter.saveRAW(document, raw_location)
        return raw_location

    def save_md_chunks(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        md_chunks_location = str((self._get_kb_location(username, kb_name) / "md_chunks" / Path(doc_name).stem).resolve())
        self.storage_adapter.save_md_chunks(chunks, md_chunks_location)
        return md_chunks_location

    def save_text_chunks(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        text_chunks_location = str((self._get_kb_location(username, kb_name) / "text_chunks" / Path(doc_name).stem).resolve())
        self.storage_adapter.save_text_chunks(chunks, text_chunks_location)
        return text_chunks_location
