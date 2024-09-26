from file_api.core.ports.file_storage_port import FileStoragePort
from fastapi import UploadFile


class FileService:
    def __init__(self, file_storage: FileStoragePort):
        self.file_storage = file_storage

    async def save_file(self, file: UploadFile, file_name: str) -> str:
        # Check if the file is a PDF
        if not file_name.lower().endswith('.pdf'):
            raise ValueError("Only PDF files are allowed")

        path = "../../../data/raw/pdf/test.pdf"

        return await self.file_storage.save_file(file, file_name, path)
