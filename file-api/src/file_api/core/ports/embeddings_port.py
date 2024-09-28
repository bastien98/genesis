from abc import ABC, abstractmethod
from langchain_core.documents import Document
from file_api.core.domain.embeddings_model import Embeddings


class EmbeddingsPort(ABC):
    @abstractmethod
    async def create_embeddings(self, chunks: list[Document]) -> Embeddings:
        pass
