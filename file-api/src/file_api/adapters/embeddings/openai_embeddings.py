from langchain_core.documents import Document
from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.ports.embeddings_port import EmbeddingsPort
from openai import AsyncOpenAI


class OpenAIEmbeddingsClient(EmbeddingsPort):
    def __init__(self, embeddings_model: str):
        self.embeddings_model = embeddings_model
        self.aclient = AsyncOpenAI()

    async def create_embeddings(self, chunks: list[Document]) -> Embeddings:
        chunked_text = [chunk.page_content for chunk in chunks]

        response = await self.aclient.embeddings.create(model=self.embeddings_model,
                                                        input=chunked_text)
        embeddings = [emb.embedding for emb in response.data]
        return Embeddings(embeddings)
