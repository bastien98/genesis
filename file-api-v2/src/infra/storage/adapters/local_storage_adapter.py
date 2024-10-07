import os

from file_api import config
from file_api_v2.ports.storage_port import StoragePort


class LocalFileStorageAdapter(StoragePort):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = config.PROCESSED_FILE_LOCATION

    def saveRAW(self, document: bytes, location: str) -> None:
        directory = os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Directory created: {directory}")
        else:
            print(f"[INFO] Directory already exists: {directory}")

        with open(location, 'wb') as f:
            f.write(document)
            print(f"Document saved at {location}")

    def saveCLEAN(self, chunks: list[str], location: str) -> None:
        directory = location if os.path.isdir(location) else os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(location, exist_ok=True)
            print(f"[INFO] Directory created: {location}")
        else:
            print(f"[INFO] Directory already exists: {location}")

        # Save each chunk in a numbered markdown file
        for index, chunk in enumerate(chunks, start=1):
            chunk_filename = f"chunk_{index}.md"
            chunk_path = os.path.join(location, chunk_filename)
            with open(chunk_path, 'w') as chunk_file:
                chunk_file.write(chunk)
            print(f"[INFO] Saved chunk {index} to {chunk_path}")

