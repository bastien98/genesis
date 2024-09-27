import os
from abc import ABC
from pathlib import Path
import aiofiles
from langchain_core.documents import Document

from file_api.core.ports.file_storage_port import FileStoragePort, FileLocation


class LocalFileStorageAdapter(FileStoragePort):

    def calculate_clean_output_location(self, filename: str) -> FileLocation:
        clean_source = (Path(os.getcwd()) / "../../../data/processed/markdown").resolve()
        return FileLocation(source=str(clean_source), filename=str(Path(filename).with_suffix(".md")))

    def _calculate_raw_output_location(self, filename: str) -> FileLocation:
        source = (Path(os.getcwd()) / "../../../data/raw/pdf").resolve()
        return FileLocation(source=str(source), filename=filename)

    async def save_raw_content(self, file: bytes, filename: str) -> None:
        raw_location = self._calculate_raw_output_location(filename)
        async with aiofiles.open(str(raw_location.full_path), 'wb') as out_file:
            await out_file.write(file)

    async def save_clean_document(self, document: Document, filename: str) -> None:
        clean_file_location = self.calculate_clean_output_location(filename)
        with open(str(clean_file_location.full_path), 'w', encoding='utf-8') as f:
            f.write(document.page_content)