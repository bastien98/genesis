import os
import pickle
from pathlib import Path
import aiofiles
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from file_api import config
from file_api.core.domain.file_location import DirectoryLocation
from file_api.core.ports.file_storage_port import FileStoragePort, DocumentLocation


class LocalFileStorageAdapter(FileStoragePort):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = config.PROCESSED_FILE_LOCATION

    def get_clean_output_location(self, filename: str, kb_id: str) -> DocumentLocation:
        clean_source = (self._get_kb_location(kb_id).source / Path(filename).stem / "markdown").resolve()
        return DocumentLocation(source=str(clean_source), filename=str(Path(filename).with_suffix(".md")))

    def _get_raw_output_location(self, filename: str, kb_id: str) -> DocumentLocation:
        source = (Path(os.getcwd()) / self.PROCESSED_FILE_LOCATION / kb_id / Path(filename).stem / "raw").resolve()
        return DocumentLocation(source=str(source), filename=filename)

    def _get_kb_location(self, kb_id: str) -> DirectoryLocation:
        source = (Path(os.getcwd()) / self.PROCESSED_FILE_LOCATION / kb_id).resolve()
        return DirectoryLocation(source=str(source))

    async def save_raw_content(self, file: bytes, filename: str, kb_id) -> None:
        raw_location = self._get_raw_output_location(filename, kb_id).full_path
        async with aiofiles.open(str(raw_location), 'wb') as out_file:
            await out_file.write(file)

    async def save_clean_document(self, document: Document, filename: str, kb_id: str) -> None:
        clean_file_location = self.get_clean_output_location(filename, kb_id)
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

    async def save_BM25_index(self, index: BM25Okapi, kb_id: str) -> None:
        with open(self._get_index_m25_location(kb_id).full_path, 'wb') as f:
            pickle.dump(index, f)

    def _get_index_m25_location(self, kb_id: str) -> DocumentLocation:
        index_source = (self._get_kb_location(kb_id).source / "bm25_index").resolve()
        return DocumentLocation(source=str(index_source), filename=self.BM25_INDEX_FILENAME)

    async def get_BM25_index(self, kb_id: str) -> BM25Okapi:
        """Load the BM25 index from specified kb_id from storage and return the BM25Okapi object."""
        # Get the BM25 index location
        bm25_index_location = self._get_index_m25_location(kb_id)

        # Load the BM25 index from the file
        if bm25_index_location.full_path.exists():
            with open(str(bm25_index_location.full_path), 'rb') as f:
                bm25_index = pickle.load(f)
                return bm25_index
        else:
            raise FileNotFoundError(f"BM25 index file for kb_id {kb_id} not found at {bm25_index_location.full_path}")

