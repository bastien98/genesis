from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.vector_db_port import VectorDbPort


class ChatService:
    def __init__(self, vector_db: VectorDbPort, file_storage: FileStoragePort):
        self._vector_db = vector_db
        self._file_storage = file_storage

    async def process(self, query: str, kb_id: str) -> str:
        vector_db_retriever = await self._vector_db.get_vector_db_retriever(kb_id, 100)
        BM25_index = await self._file_storage.get_BM25_index(kb_id)
        BM25_index.get_scores(query.split())
        return "ok"
