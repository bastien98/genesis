from langchain_core.documents import Document
from openai import AsyncOpenAI
from langchain_openai import OpenAIEmbeddings

from domain.entities.embeddings import Embeddings
from ports.embeddings_port import EmbeddingsPort


class OpenAIEmbeddingsClient(EmbeddingsPort):
    def __init__(self, embeddings_model: OpenAIEmbeddings):
        self.embeddings_model = embeddings_model
        self.aclient = AsyncOpenAI()

    async def create_embeddings(self, chunks: list[Document]) -> Embeddings:
        chunked_text = [chunk.page_content for chunk in chunks]

        response = await self.aclient.embeddings.create(model=self.embeddings_model.model,
                                                        input=chunked_text)
        embeddings = [emb.embedding for emb in response.data]
        return Embeddings(embeddings, self.embeddings_model)
