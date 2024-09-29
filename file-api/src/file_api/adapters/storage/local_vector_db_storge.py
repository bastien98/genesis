from chromadb import AsyncHttpClient as ChromaClient
from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.ports.vector_db_port import VectorDbPort
import chromadb.utils.embedding_functions as embedding_functions


class LocalChromaDbAdapter(VectorDbPort):
    def __init__(self, aclient: ChromaClient):
        self.aclient = aclient

    async def save_embeddings(self, embeddings: Embeddings, vector_db_index: str) -> None:
        """
        Saves the embeddings of all chunks of a document into the specified vector database index.
           Args:
               embeddings (Embeddings): The embeddings to be saved, representing the document's chunked data.
               vector_db_index (str): The index in the vector database where the embeddings will be stored.
           Returns:
            None
       """
        chroma_ef = embedding_functions.create_langchain_embedding(embeddings.embeddings_model)
        collection = self.aclient.create_collection(name=vector_db_index, embedding_function=chroma_ef)
        collection.add(embeddings.embeddings)
