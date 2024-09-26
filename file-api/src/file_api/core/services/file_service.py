
from file_api.core.domain.ex_document import ExDocument
from file_api.core.ports.file_storage_port import FileStoragePort


class FileService:
    def __init__(self, file_storage: FileStoragePort):
        self.file_storage = file_storage

    async def save_ex_document(self, document: ExDocument):
        # Check if the file is a PDF
        # if not file.name.lower().endswith('.pdf'):
        #     raise ValueError("Only PDF files are allowed")

        await self.file_storage.save_document_to_raw(document)
        return document.name



