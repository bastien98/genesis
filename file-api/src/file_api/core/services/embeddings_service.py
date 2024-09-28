from langchain_core.documents import Document
from file_api.core.ports.embeddings_port import EmbeddingsPort


class EmbeddingsService:
    def __init__(self, client: EmbeddingsPort):
        self.client = client

    async def create_embeddings(self, chunks: list[Document]) -> list[list[float]]:
        embeddings = await self.client.create_embeddings(chunks)
        return embeddings
