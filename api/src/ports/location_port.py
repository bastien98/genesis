from abc import ABC, abstractmethod
from pathlib import Path


class LocationPort(ABC):
    @property
    @abstractmethod
    def PROCESSED_FILE_LOCATION(self) -> Path:
        """Path on the filesystem where processed files are stored."""
        pass

    @property
    @abstractmethod
    def BM25_INDEX_FILENAME(self) -> str:
        """Filename for the BM25 index."""
        pass

    @abstractmethod
    def get_user_location(self, user_id: int) -> Path:
        """Retrieve the path for the user's base directory."""
        pass

    @abstractmethod
    def get_kb_location(self, user_id: int, kb_id: int) -> Path:
        """Retrieve the path for the specific knowledge base directory."""
        pass

    @abstractmethod
    def get_raw_doc_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        """Retrieve the path for the raw document storage location."""
        pass

    @abstractmethod
    def get_md_chunks_doc_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        """Retrieve the path for markdown chunk storage location."""
        pass

    @abstractmethod
    def get_text_chunks_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        """Retrieve the path for text chunk storage location."""
        pass

    @abstractmethod
    def get_bm25_index_location(self, user_id: int, kb_id: int) -> str:
        """Retrieve the path for the BM25 index storage location."""
        pass
