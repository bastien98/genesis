from file_api.adapters.storage.local_storage_adapter import LocalFileStorageAdapter
from file_api.core.services.file_service import FileService


def get_file_service() -> FileService:
    return FileService(LocalFileStorageAdapter())
