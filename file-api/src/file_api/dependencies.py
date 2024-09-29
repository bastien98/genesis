import os

from file_api.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsClient
from file_api.adapters.parsers.llama_parser import LlamaParser
from file_api.adapters.parsers.pdf_parser import PdfParser
from file_api.adapters.storage.local_file_storage_adapter import LocalFileStorageAdapter
from file_api.core.domain.chunkers import HeaderChunker
from file_api.core.domain.indexing import bm25_simple
from file_api.core.services.embeddings_service import EmbeddingsService
from file_api.core.services.file_service import FileStorageService
from file_api.core.services.kb_service import KBService

EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL', 'text-embedding-ada-002')

file_storage_adapter = LocalFileStorageAdapter()


def get_file_service() -> FileStorageService:
    return FileStorageService(file_storage_adapter, LlamaParser(), HeaderChunker())


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(OpenAIEmbeddingsClient(EMBEDDINGS_MODEL))


def get_kb_service() -> KBService:
    return KBService(file_storage_adapter, bm25_simple)
