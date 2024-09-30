from file_api.core.ports.vector_db_port import VectorDbPort


class ChatService:
    def __init__(self, vector_db: VectorDbPort):
        self._vector_db = vector_db

    async def process(self, query: str, kb_id: str) -> str:
        vector_db_retriever = await self._vector_db.get_retriever(kb_id, 100)
        vector_db_retriever.invoke(query)
        return "ok"
