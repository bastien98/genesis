from abc import ABC, abstractmethod
from langchain_core.documents import Document


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
