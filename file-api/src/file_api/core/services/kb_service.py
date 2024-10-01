from file_api.core.ports.chunker_port import ChunkerPort
from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.indexing_port import BM25IndexingStrategy
from file_api.core.ports.vector_db_port import VectorDbPort
from langchain_core.documents import Document


class KBService:
    def __init__(self, file_storage: FileStoragePort, bm25_index_creator: BM25IndexingStrategy, vector_db: VectorDbPort,
                 chunker: ChunkerPort):
        self.file_storage = file_storage
        self.create_bm25_index = bm25_index_creator
        self.vector_db = vector_db
        self.chunker = chunker

    async def update(self, md_chunks: list[Document], kb_id: str) -> None:
        await self.vector_db.save_chunks(md_chunks, kb_id)
        # await self.file_storage.create_BM25_index(kb_id)