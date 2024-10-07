import os
from abc import abstractmethod
from pathlib import Path
from file_api_v2.ports.storage_port import StoragePort


class AbstractDocumentManager:
    @abstractmethod
    def saveRAW(self, document: bytes, doc_name: str, username: str, kb_name: str) -> str:
        pass

    @abstractmethod
    def saveCLEAN(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        pass


class LocalFileSystemDocumentManager(AbstractDocumentManager):

    def __init__(self, storage_adapter: StoragePort):
        self.storage_adapter = storage_adapter

    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path("../../../data/processed")).resolve()

    def _get_kb_location(self, kb_name: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / kb_name).resolve()
        return kb_location

    def saveRAW(self, document: bytes, doc_name: str, username: str, kb_name: str) -> str:
        raw_location = str((self._get_kb_location(kb_name) / "raw" / "pdf" / doc_name).resolve())
        self.storage_adapter.saveRAW(document, raw_location)
        return raw_location

    def saveCLEAN(self, chunks: list[str], doc_name: str, username: str, kb_name: str) -> str:
        clean_location = str((self._get_kb_location(kb_name) / "clean" / Path(doc_name).stem).resolve())
        self.storage_adapter.saveCLEAN(chunks, clean_location)
        return clean_location

