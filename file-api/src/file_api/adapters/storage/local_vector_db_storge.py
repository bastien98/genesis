from langchain_community.vectorstores import Chroma
from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.ports.vector_db_port import VectorDbPort


class LocalChromaDbAdapter(VectorDbPort):
    def __init__(self, embeddings: Embeddings):
        self.vector_db = Chroma(
            persist_directory="../../../data/chroma_db",
            embedding_function=embeddings.embeddings_model

        )

    async def save_embeddings(self, embeddings: Embeddings, vector_db_index: str) -> None:
        """
        Saves the embeddings of all chunks of a document into the specified vector database (vectorDB) index.
           Args:
               embeddings (Embeddings): The embeddings to be saved, representing the document's chunked data.
               vector_db_index (str): The index in the vector database where the embeddings will be stored.
           Returns:
            None
       """
        # self.vector_db.get_or_create_collection(
        #     name=vector_db_index,  # The name of the collection you want to save to
        #     embedding_function=embedding_fn,
        # )
        #
        # # Insert embeddings with metadata (you can customize this)
        # collection.add(
        #     embeddings=embeddings,
        #     metadatas=metadata
        # )

    pass
