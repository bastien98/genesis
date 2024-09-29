import uuid
from typing import Union
from chromadb import AsyncHttpClient as ChromaClient
from file_api.core.ports.vector_db_port import VectorDbPort
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


class LocalChromaDbAdapter(VectorDbPort):
    def __init__(self, aclient: ChromaClient, model: Union[OpenAIEmbeddings, OllamaEmbeddings]):
        self.aclient = aclient
        self.model = model

    async def save_chunks(self, chunks: list[Document], kb_id: str) -> None:
        chroma_ef = embedding_functions.create_langchain_embedding(self.model)
        # collection = self.aclient.create_collection(name=kb_id, embedding_function=chroma_ef)
        collection = self.aclient.get_collection(name=kb_id, embedding_function=chroma_ef)
        chunks_text = [chunk.page_content for chunk in chunks]
        chunk_ids = [str(uuid.uuid4()) for _ in chunks_text]
        # You can store chunks with associated metadata (e.g., source document, page number) if you want to track the origin or location of each chunk
        collection.add(documents=chunks_text, ids=chunk_ids)
