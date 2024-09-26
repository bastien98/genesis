import os
from pathlib import Path

import aiofiles

from langchain_core.documents import Document
from file_api.core.ports.file_storage_port import FileStoragePort


class LocalFileStorageAdapter(FileStoragePort):
    async def save_raw_document(self, file: bytes, filename: str) -> str:
        file_location = (Path(os.getcwd()) / "../../../data/raw/pdf" / filename).resolve()
        async with aiofiles.open(file_location, 'wb') as out_file:
            await out_file.write(file)
        return str(file_location)

