from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.indexing_port import BM25IndexingStrategy
from file_api.core.ports.vector_db_port import VectorDbPort
from langchain_core.documents import Document


class KBService:
    def __init__(self, file_storage: FileStoragePort, bm25_index_creator: BM25IndexingStrategy, vector_db: VectorDbPort):
        self.file_storage = file_storage
        self.create_bm25_index = bm25_index_creator
        self.vector_db = vector_db

    async def update(self, filename: str, chunks: list[Document], vector_db_index: str) -> None:
        await self._update_BM25_index(filename)
        await self._add_to_vector_db(chunks, vector_db_index)

    async def _update_BM25_index(self, filename: str) -> None:
        documents = await self.file_storage.read_directory(
            self.file_storage.get_clean_output_location(filename).get_directory_location)
        bm25_index = self.create_bm25_index(documents)
        await self.file_storage.save_BM25_index(bm25_index, filename)

    async def _add_to_vector_db(self, chunks: list[Document], vector_db_index: str) -> None:
        await self.vector_db.save_chunks(chunks, vector_db_index)
