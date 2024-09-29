import os
import pickle
from pathlib import Path
import aiofiles
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from file_api.core.domain.file_location import DirectoryLocation
from file_api.core.ports.file_storage_port import FileStoragePort, DocumentLocation


class LocalFileStorageAdapter(FileStoragePort):
    BM25_INDEX_FILENAME = "knowledge_base.pkl"

    def get_clean_output_location(self, filename: str) -> DocumentLocation:
        clean_source = (Path(os.getcwd()) / "../../../data/processed/markdown").resolve()
        return DocumentLocation(source=str(clean_source), filename=str(Path(filename).with_suffix(".md")))

    def _get_raw_output_location(self, filename: str) -> DocumentLocation:
        source = (Path(os.getcwd()) / "../../../data/raw/pdf").resolve()
        return DocumentLocation(source=str(source), filename=filename)

    async def save_raw_content(self, file: bytes, filename: str) -> None:
        raw_location = self._get_raw_output_location(filename)
        async with aiofiles.open(str(raw_location.full_path), 'wb') as out_file:
            await out_file.write(file)

    async def save_clean_document(self, document: Document, filename: str) -> None:
        clean_file_location = self.get_clean_output_location(filename)
        with open(str(clean_file_location.full_path), 'w', encoding='utf-8') as f:
            f.write(document.page_content)

    async def read_directory(self, location: DirectoryLocation) -> list[Document]:
        directory_path = location.source
        documents = []
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                    content = await f.read()
                    documents.append(Document(page_content=content))

        return documents

    async def save_BM25_index(self, index: BM25Okapi, filename: str) -> None:
        with open(self._get_index_m25_location().full_path, 'wb') as f:
            pickle.dump(index, f)

    def _get_index_m25_location(self) -> DocumentLocation:
        index_source = (Path(os.getcwd()) / "../../../data/processed/bm25_index").resolve()
        return DocumentLocation(source=str(index_source), filename=self.BM25_INDEX_FILENAME)
