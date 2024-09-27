from file_api.adapters.parser.llama_parser import LlamaParser
from file_api.adapters.parser.pdf_parser import PdfParser
from file_api.adapters.storage.local_storage_adapter import LocalFileStorageAdapter
from file_api.core.services.file_service import FileStorageService


def get_file_service() -> FileStorageService:
    return FileStorageService(LocalFileStorageAdapter(), PdfParser(), LlamaParser())
