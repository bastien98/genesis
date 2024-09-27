import os
from pathlib import Path
import aiofiles
from langchain_core.documents import Document

from file_api.core.ports.file_storage_port import FileStoragePort, FileLocation


class LocalFileStorageAdapter(FileStoragePort):

    async def save_raw_content(self, file: bytes, filename: str) -> FileLocation:
        source = (Path(os.getcwd()) / "../../../data/raw/pdf").resolve()
        filepath = (source / filename).resolve()
        async with aiofiles.open(filepath, 'wb') as out_file:
            await out_file.write(file)
        return FileLocation(source=str(source), filename=filename)

    async def save_clean_document(self, document: Document, raw_file_location: FileLocation) -> FileLocation:
        def _transform_path(raw_path: FileLocation) -> Path:
            """
            Transforms a part of the path in the 'source' from 'raw' to 'clean'
            and ensures the file has a '.md' extension.
            """
            raw_path = Path(raw_path.full_path)
            parts = list(raw_path.parts)
            new_parts = [part if part != 'raw' else 'processed' for part in parts]
            new_path = Path(*new_parts)
            if new_path.suffix != '.md':
                new_path = new_path.with_suffix('.md')
            return new_path

        clean_path = _transform_path(raw_file_location)

        with open(clean_path, 'w', encoding='utf-8') as f:
            f.write(document.page_content)

        return FileLocation(source=str(clean_path.parent), filename=clean_path.name)



