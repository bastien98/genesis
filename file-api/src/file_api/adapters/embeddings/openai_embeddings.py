from enum import Enum
from langchain_core.documents import Document
from file_api.core.ports.embeddings_port import EmbeddingsPort
import openai


class OpenAIEmbeddingModel(str, Enum):
    ADA_002 = "text-embedding-ada-002"


class OpenAIEmbeddingsClient(EmbeddingsPort):
    def __init__(self, embeddings_model: OpenAIEmbeddingModel):
        self.embeddings_model = embeddings_model

    async def create_embeddings(self, chunks: list[Document]) -> list[list[float]]:
        chunked_text = [chunk.page_content for chunk in chunks]

        response = await openai.Embedding.acreate(
            model=self.embeddings_model.ADA_002,
            input=chunked_text
        )
        return response
