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

    # Get Directory location methods
    def get_kb_location(self, kb_id: str) -> DirectoryLocation:
        source = (Path(os.getcwd()) / self.PROCESSED_FILE_LOCATION / kb_id).resolve()
        return DirectoryLocation(source=str(source))

    def get_kb_files_location(self, kb_id: str) -> DirectoryLocation:
        source = (Path(os.getcwd()) / self.PROCESSED_FILE_LOCATION / kb_id / "files").resolve()
        return DirectoryLocation(source=str(source))

    # Get Document location methods
    def get_BM25_index_location(self, kb_id: str) -> DocumentLocation:
        bm25_index_source = (self.get_kb_files_location(kb_id).source / "bm25_index").resolve()
        return DocumentLocation(source=str(bm25_index_source), filename="bm25_index.pkl")

    def get_markdown_location(self, filename: str, kb_id: str) -> DocumentLocation:
        markdown_source = (self.get_kb_files_location(kb_id).source / Path(filename).stem / "markdown").resolve()
        return DocumentLocation(source=str(markdown_source), filename=str(Path(filename).with_suffix(".md")))

    def get_raw_location(self, filename: str, kb_id: str) -> DocumentLocation:
        raw_source = (self.get_kb_files_location(kb_id).source / Path(filename).stem / "raw").resolve()
        return DocumentLocation(source=str(raw_source), filename=filename)

    def get_text_location(self, filename: str, kb_id: str) -> DocumentLocation:
        text_source = (self.get_kb_files_location(kb_id).source / Path(filename).stem / "text").resolve()
        return DocumentLocation(source=str(text_source), filename=str(Path(filename).with_suffix(".txt")))

    # Save files to Document location methods
    def save_BM25_index(self, bm25_index: BM25Okapi, kb_id: str) -> None:
        bm25_source = self.get_BM25_index_location(kb_id).full_path
        with open(str(bm25_source), 'wb') as f:
            pickle.dump(bm25_index, f)

    def save_markdown_document(self, document: Document, filename: str, kb_id: str) -> None:
        markdown_file_location = self.get_markdown_location(filename, kb_id).full_path
        with open(str(markdown_file_location), 'w', encoding='utf-8') as f:
            f.write(document.page_content)
            print(f"Document saved at {markdown_file_location}")

    def save_raw_document(self, file: bytes, filename: str, kb_id) -> None:
        raw_location = self.get_raw_location(filename, kb_id).full_path
        with open(str(raw_location), 'wb') as f:
            f.write(file)
            print(f"Document saved at {raw_location}")

    def save_text_document(self, document: Document, filename: str, kb_id: str) -> None:
        text_doc_location = self.get_text_location(filename, kb_id).full_path
        with open(str(text_doc_location), 'w') as file:
            file.write(document.page_content)
            print(f"Document saved at {text_doc_location}")

    async def read_text_directory(self, location: DirectoryLocation) -> list[Document]:
        directory_path = location.source
        documents = []
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                    content = await f.read()
                    documents.append(Document(page_content=content))

        return documents

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
