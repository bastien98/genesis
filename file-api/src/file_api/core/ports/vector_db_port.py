from abc import ABC, abstractmethod
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class VectorDbPort(ABC):
    @abstractmethod
    async def save_chunks(self, chunks: list[Document], kb_id: str) -> None:
        """
        Saves all chunks of a document into the specified vector database index.
        Each index in the vector database maps directly to a kb_id.

        Args:
            chunks (list[Document]): The list of document chunks to be saved.
            kb_id (str): The index in the vector database where the chunks will be stored.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def similarity_search(self, query: str, kb_id: str, k: int) -> list[Document]:
        pass

    @abstractmethod
    async def similarity_search_with_score(self, query: str, kb_id: str, k: int) -> list[tuple[Document, float]]:
        pass

    @abstractmethod
    def get_kb_document_count(self, kb_id: str) -> int:
        pass
