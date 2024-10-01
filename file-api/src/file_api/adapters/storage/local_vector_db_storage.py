import uuid
from typing import Union, List, Tuple

import chromadb
from chromadb import AsyncHttpClient as ChromaClient
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever

from file_api import config
from file_api.core.ports.vector_db_port import VectorDbPort
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings


class LocalChromaDbAdapter(VectorDbPort):
    def __init__(self, aclient: ChromaClient, model: Union[OpenAIEmbeddings, OllamaEmbeddings]):
        self.aclient = aclient
        self.embedding_function = embedding_functions.create_langchain_embedding(model)

    @staticmethod
    def create(embeddings_model: Union[OpenAIEmbeddings, OllamaEmbeddings]):
        return LocalChromaDbAdapter(
            chromadb.PersistentClient(path=f"{config.PROCESSED_FILE_LOCATION}/vector_db"),
            embeddings_model
        )

    async def save_chunks(self, chunks: list[Document], kb_id: str) -> None:
        try:
            # Try to get the collection if it already exists
            print(f"Attempting to retrieve collection: {kb_id}")
            collection = self.aclient.get_collection(name=kb_id, embedding_function=self.embedding_function)
            print(f"Collection '{kb_id}' retrieved successfully.")
        except InvalidCollectionException:
            # If the collection doesn't exist, create it
            print(f"Collection '{kb_id}' does not exist. Creating a new one.")
            collection = self.aclient.create_collection(name=kb_id, embedding_function=self.embedding_function)
            print(f"Collection '{kb_id}' created successfully.")

        chunks_text = [chunk.page_content for chunk in chunks]
        chunk_ids = [str(uuid.uuid4()) for _ in chunks_text]
        # You can store chunks with associated metadata (e.g., source document, page number) if you want to track the origin or location of each chunk
        collection.add(documents=chunks_text, ids=chunk_ids)

    async def similarity_search(self, query: str, kb_id: str, k: int) -> list[Document]:
        """ Retrieves a vector store retriever for a given knowledge base and returns the top-k most similar chunks. """
        return Chroma(
            client=self.aclient,
            collection_name=kb_id,
            embedding_function=self.embedding_function,
        ).as_retriever(
            search_type="similarity",
            search_kwargs={"k": k}
        ).invoke(query)

    async def similarity_search_with_score(self, query: str, kb_id: str, k: int) -> list[tuple[Document, float]]:
        return Chroma(
            client=self.aclient,
            collection_name=kb_id,
            embedding_function=self.embedding_function,
        ).similarity_search_with_score(query=query, k=k)

    def get_kb_document_count(self, kb_id: str) -> int:
        return self.aclient.get_collection(name=kb_id, embedding_function=self.embedding_function).count()
