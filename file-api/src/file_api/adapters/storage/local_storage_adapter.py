import os
from file_api.core.ports.file_storage_port import FileStoragePort
from pathlib import Path
from fastapi import UploadFile
import aiofiles


class LocalFileStorageAdapter(FileStoragePort):
    async def save_file(self, file: UploadFile, file_name: str, file_path: str) -> str:
        # Ensure the directory exists
        Path(file_path).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(path, file_name)

        # Save the file to the specified path
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        return file_path
