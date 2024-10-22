import os
from pathlib import Path


class LocalLocationService:
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path("../../../data/processed")).resolve()
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"

    def get_user_location(self, username: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / username).resolve()
        return kb_location

    def get_kb_location(self, username: str, kb_name: str) -> Path:
        kb_location = self.get_user_location(username) / Path(kb_name)
        return kb_location

    def get_raw_doc_location(self, username: str, kb_name: str, doc_name: str) -> str:
        return str((self.get_kb_location(username, kb_name) / "raw" / "pdf" / doc_name).resolve())

    def get_md_chunks_doc_location(self, username: str, kb_name: str, doc_name: str) -> str:
        return str(
            (self.get_kb_location(username, kb_name) / "md_chunks" / Path(doc_name).stem).resolve())

    def get_text_chunks_location(self, username: str, kb_name: str, doc_name: str) -> str:
        return str(
            (self.get_kb_location(username, kb_name) / "text_chunks" / Path(doc_name).stem).resolve())

    def get_bm25_index_location(self, username: str, kb_name: str) -> str:
        return str((self.get_kb_location(username, kb_name) / self.BM25_INDEX_FILENAME).resolve())
