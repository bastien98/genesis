import os
from pathlib import Path

import aiofiles

from file_api.core.domain.ex_document import ExDocument
from file_api.core.ports.file_storage_port import FileStoragePort


class LocalFileStorageAdapter(FileStoragePort):
    async def save_document_to_raw(self, file: ExDocument):
        file_path = (Path(os.getcwd()) / "../../../data/raw/pdf" / file.name).resolve()
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(file.content)
