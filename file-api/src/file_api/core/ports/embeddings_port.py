from abc import ABC, abstractmethod
from langchain_core.documents import Document


class EmbeddingsPort(ABC):
    @abstractmethod
    async def create_embeddings(self, chunks: list[Document]) -> list[list[float]]:
        pass
