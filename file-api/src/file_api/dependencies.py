import os

from file_api.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsClient
from file_api.adapters.parsers.llama_parser import LlamaParser
from file_api.adapters.parsers.pdf_parser import PdfParser
from file_api.adapters.storage.local_storage_adapter import LocalFileStorageAdapter
from file_api.core.domain.chunkers import HeaderChunker
from file_api.core.services.embeddings_service import EmbeddingsService
from file_api.core.services.file_service import FileStorageService

EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL', 'text-embedding-ada-002')


def get_file_service() -> FileStorageService:
    return FileStorageService(LocalFileStorageAdapter(), PdfParser(), LlamaParser(), HeaderChunker())


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(OpenAIEmbeddingsClient(EMBEDDINGS_MODEL))
