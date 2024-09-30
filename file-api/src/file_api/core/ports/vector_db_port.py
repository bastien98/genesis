from abc import ABC, abstractmethod

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever


class VectorDbPort(ABC):
    @abstractmethod
    async def save_chunks(self, chunks: list[Document], kb_id: str) -> None:
        """
        Saves all chunks of a document into the specified vector database index.

        Args:
            chunks (list[Document]): The list of document chunks to be saved.
            kb_id (str): The index in the vector database where the chunks will be stored.

        Returns:
            None
        """
        pass

    @abstractmethod
    async def get_vector_db_retriever(self, kb_id: str, k: int) -> VectorStoreRetriever:
        pass
