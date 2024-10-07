import os
from abc import abstractmethod
from pathlib import Path
from file_api_v2.ports.storage_port import StoragePort
from file_api_v2.ports.vector_db_port import VectorDbPort


class VectorDbManager():

    def __init__(self, vectordb_adapter: VectorDbPort):
        self.vectordb_adapter = vectordb_adapter

    async def save_chunks_to_kb(self, chunks: list[str], username: str, kb_name:str) -> None:
        await self.vectordb_adapter.save_chunks(chunks, username, kb_name)
