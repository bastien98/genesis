import os
from pathlib import Path
import config
from ports.location_port import LocationPort


class LocalLocationAdapter(LocationPort):
    PROCESSED_FILE_LOCATION = (Path(os.getcwd()) / Path(config.PROCESSED_FILE_LOCATION)).resolve()
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"

    def get_user_location(self, username: str) -> Path:
        kb_location = (self.PROCESSED_FILE_LOCATION / username).resolve()
        return kb_location

    def get_kb_location(self, username: str, kb_id: int) -> Path:
        kb_location = self.get_user_location(username) / Path(str(kb_id))
        return kb_location

    def get_raw_doc_location(self, username: str, kb_id: int, doc_name: str) -> str:
        return str((self.get_kb_location(username, kb_id) / "raw" / "pdf" / doc_name).resolve())

    def get_md_chunks_doc_location(self, username: str, kb_id: int, doc_name: str) -> str:
        return str(
            (self.get_kb_location(username, kb_id) / "md_chunks" / Path(doc_name).stem).resolve())

    def get_text_chunks_location(self, username: str, kb_id: int, doc_name: str) -> str:
        return str(
            (self.get_kb_location(username, kb_id) / "text_chunks" / Path(doc_name).stem).resolve())

    def get_bm25_index_location(self, username: str, kb_id: int) -> str:
        return str((self.get_kb_location(username, kb_id) / self.BM25_INDEX_FILENAME).resolve())
