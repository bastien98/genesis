from typing import List
from domain.entities.raw_document import RawDocument
from ports.storage_port import FileStoragePort


class FileStorageService:
    def __init__(self, storage_adapter: FileStoragePort):
        self.store = storage_adapter

    def store_raw_document(self, raw_doc: RawDocument, location: str) -> None:
        self.store.save_raw_file(raw_doc.content, location)

    def save_text_chunks(self, text_chunks: List[str], location: str) -> None:
        self.store.save_text_chunks(text_chunks, location)

    def save_md_chunks(self, text_chunks: List[str], location: str) -> None:
        self.store.save_md_chunks(text_chunks, location)
