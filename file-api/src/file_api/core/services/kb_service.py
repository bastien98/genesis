from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.indexing_port import BM25IndexingStrategy
from file_api.core.ports.vector_db_port import VectorDbPort
from langchain_core.documents import Document


class KBService:
    def __init__(self, file_storage: FileStoragePort, bm25_index_creator: BM25IndexingStrategy, vector_db: VectorDbPort):
        self.file_storage = file_storage
        self.create_bm25_index = bm25_index_creator
        self.vector_db = vector_db

    async def update(self, filename: str, chunks: list[Document], kb_id: str) -> None:
        await self._update_BM25_index(filename, kb_id)
        await self._add_to_vector_db(chunks, kb_id)

    async def _update_BM25_index(self, filename: str, kb_id: str) -> None:
        documents = await self.file_storage.read_directory(
            self.file_storage.get_clean_output_location(filename, kb_id).get_directory_location)
        bm25_index = self.create_bm25_index(documents)
        await self.file_storage.save_BM25_index(bm25_index, filename, kb_id)

    async def _add_to_vector_db(self, chunks: list[Document], kb_id: str) -> None:
        await self.vector_db.save_chunks(chunks, kb_id)
