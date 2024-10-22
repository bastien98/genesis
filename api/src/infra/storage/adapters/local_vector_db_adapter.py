import uuid
from typing import Union
import chromadb
from chromadb import AsyncHttpClient as ChromaClient
from chromadb.errors import InvalidCollectionException
from langchain_chroma import Chroma
import chromadb.utils.embedding_functions as embedding_functions
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings

import config
from ports.vector_db_port import VectorDbPort


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

    async def save_chunks(self, chunks: list[str], username: str, kb_name: str, doc_name: str) -> None:
        collection = f"{username}_{kb_name}"
        try:
            # Try to get the collection if it already exists
            print(f"Attempting to retrieve collection: {collection}")
            collection = self.aclient.get_collection(name=collection, embedding_function=self.embedding_function)
            print(f"Collection '{collection}' retrieved successfully.")
        except InvalidCollectionException:
            # If the collection doesn't exist, create it
            print(f"Collection '{collection}' does not exist. Creating a new one.")
            collection = self.aclient.create_collection(name=collection, embedding_function=self.embedding_function)
            print(f"Collection '{collection}' created successfully.")

        chunk_ids = [str(uuid.uuid4()) for _ in chunks]
        # You can store chunks with associated metadata (e.g., source document, page number) if you want to track the origin or location of each chunk
        metadata = [
            {"filename": doc_name, "chunk_number": chunk_num}  # Metadata with filename and chunk number
            for chunk_num, _ in enumerate(chunks, start=1)
        ]
        collection.add(documents=chunks, ids=chunk_ids, metadatas=metadata)

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
