from abc import ABC, abstractmethod
from typing import List

from file_api_v2.domain.entities import Document, User, KnowledgeBase, Chunk, BM25Index, RawDocument


class RawDocumentRepository(ABC):
    @abstractmethod
    def save_raw_document(self, document: RawDocument, user: User, kb: KnowledgeBase) -> None:
        pass

    @abstractmethod
    def get_raw_document(self, name: str, user: User, kb: KnowledgeBase) -> RawDocument:
        pass


class ChunkRepository(ABC):
    @abstractmethod
    def save_chunks(self, chunks: List[Chunk], document: Document, user: User, kb: KnowledgeBase) -> None:
        pass

    @abstractmethod
    def get_chunks(self, document: Document, user: User, kb: KnowledgeBase) -> List[Chunk]:
        pass


class BM25IndexRepository(ABC):
    @abstractmethod
    def save_index(self, bm25_index: BM25Index, user: User, kb: KnowledgeBase) -> None:
        pass

    @abstractmethod
    def get_index(self, user: User, kb: KnowledgeBase) -> BM25Index:
        pass
