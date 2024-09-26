from langchain_core.documents import Document
from file_api.core.ports.file_storage_port import FileStoragePort


class FileService:
    def __init__(self, file_storage: FileStoragePort):
        self.file_storage = file_storage

    async def save_raw_document(self, document: bytes, filename: str) -> str:
        return await self.file_storage.save_raw_document(document, filename)



