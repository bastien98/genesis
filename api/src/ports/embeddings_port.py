from abc import ABC, abstractmethod
from langchain_core.documents import Document

from domain.entities.embeddings import Embeddings


class EmbeddingsPort(ABC):
    @abstractmethod
    async def create_embeddings(self, chunks: list[Document]) -> Embeddings:
        pass
