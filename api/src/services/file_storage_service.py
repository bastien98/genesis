from typing import List

from rank_bm25 import BM25Okapi

from domain.entities.raw_document import RawDocument
from ports.file_storage_port import FileStoragePort


class FileStorageService:
    def __init__(self, storage_adapter: FileStoragePort):
        self.storage_adapter = storage_adapter

    def save_raw_document(self, raw_doc: RawDocument, location: str) -> None:
        self.storage_adapter.save_raw_file(raw_doc.content, location)

    def save_text_chunks(self, text_chunks: List[str], location: str) -> None:
        self.storage_adapter.save_text_chunks(text_chunks, location)

    def read_text_chunks(self, location: str) -> list[str]:
        return self.storage_adapter.read_text_chunks(location)

    def save_md_chunks(self, text_chunks: List[str], location: str) -> None:
        self.storage_adapter.save_md_chunks(text_chunks, location)

    def save_BM25_index(self, bm25_index: BM25Okapi, location: str) -> None:
        self.storage_adapter.save_BM25_index(bm25_index, location)

    def read_BM25_index(self, location: str) -> BM25Okapi:
        return self.storage_adapter.read_BM25_index(location)
