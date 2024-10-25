from abc import ABC, abstractmethod
from langchain_core.documents import Document


class VectorDbPort(ABC):
    @abstractmethod
    async def save_chunks(self, chunks: list[str], kb_id: int, doc_name: str) -> None:
        """
        Saves all chunks of a document into the specified vector database index.
        Each index in the vector database maps directly to a kb_id.
        """
        pass

    @abstractmethod
    async def similarity_search(self, query: str, kb_id: str, k: int) -> list[Document]:
        pass

    @abstractmethod
    async def similarity_search_with_score(self, query: str, kb_id: int, k: int) -> list[tuple[Document, float]]:
        pass

    @abstractmethod
    def get_kb_document_count(self, kb_id: int) -> int:
        pass
