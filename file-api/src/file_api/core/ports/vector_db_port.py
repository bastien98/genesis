from abc import ABC, abstractmethod

from file_api.core.domain.embeddings_model import Embeddings


class EmbeddingsPort(ABC):
    @abstractmethod
    async def save_embeddings(self, embeddings: Embeddings, vector_db_index: str) -> None:
        pass
