import os

from file_api import config
from file_api_v2.ports.storage_port import StoragePort


class LocalFileStorageAdapter(StoragePort):
    BM25_INDEX_FILENAME = "knowledge_base_bm25_index.pkl"
    PROCESSED_FILE_LOCATION = config.PROCESSED_FILE_LOCATION

    def savePDF(self, document: bytes, location: str) -> None:
        directory = os.path.dirname(location)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Directory created: {directory}")
        else:
            print(f"[INFO] Directory already exists: {directory}")

        with open(location, 'wb') as f:
            f.write(document)
            print(f"Document saved at {location}")
