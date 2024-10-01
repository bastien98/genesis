import json
import os
from enum import StrEnum
from file_api.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsClient
from file_api.adapters.parsers.llama_parser import LlamaParser
from file_api.adapters.parsers.pdf_parser import PdfParser
from file_api.adapters.storage.local_file_storage_adapter import LocalFileStorageAdapter
from file_api.adapters.storage.local_vector_db_storage import LocalChromaDbAdapter
from file_api.core.domain.chunkers import HeaderChunker
from file_api.core.domain.indexing import bm25_simple
from file_api.core.services.embeddings_service import EmbeddingsService
from file_api.core.services.file_service import FileStorageService
from file_api.core.services.kb_service import KBService
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import chromadb

from file_api.core.services.chat_service import ChatService

load_dotenv()


class Model(StrEnum):
    OPENAI = "openai"
    OLLAMA = "ollama"


# Default to OpenAI if MODEL is not defined or invalid
model_env = os.getenv('MODEL', '{"openai": "text-embedding-ada-002"}')
try:
    embeddings_model_env = json.loads(model_env)
except json.JSONDecodeError:
    print(f"Invalid JSON format in MODEL environment variable: {model_env}. Defaulting to OpenAI.")
    embeddings_model_env = {Model.OPENAI: "text-embedding-ada-002"}

# Check which model to use and set EMBEDDINGS_MODEL accordingly
if Model.OPENAI in embeddings_model_env:
    EMBEDDINGS_MODEL = OpenAIEmbeddings(model=embeddings_model_env[Model.OPENAI])
    EMBEDDINGS_CLIENT = OpenAIEmbeddingsClient(EMBEDDINGS_MODEL)
    print(f"using the OpenAI embeddings model: {embeddings_model_env[Model.OPENAI]}")
elif Model.OLLAMA in embeddings_model_env:
    EMBEDDINGS_MODEL = OllamaEmbeddings(model=embeddings_model_env[Model.OLLAMA])
    raise NotImplementedError("The 'embeddings_client' for Ollama embeddings is not implemented yet. Please implement "
                              "the client functionality.")
else:
    EMBEDDINGS_MODEL = OpenAIEmbeddings(model=embeddings_model_env[Model.OPENAI])
    EMBEDDINGS_CLIENT = OpenAIEmbeddingsClient(EMBEDDINGS_MODEL)
    print(
        f"Environment variable MODEL undefined, defaulting to OpenAI embeddings model: {embeddings_model_env[Model.OPENAI]}")

file_storage_adapter = LocalFileStorageAdapter()

chunker = HeaderChunker()


def get_file_service() -> FileStorageService:
    return FileStorageService(file_storage_adapter, LlamaParser(), PdfParser(), chunker)


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(EMBEDDINGS_CLIENT)


vector_db = LocalChromaDbAdapter.create(EMBEDDINGS_MODEL)


def get_kb_service() -> KBService:
    return KBService(file_storage_adapter, bm25_simple,
                     vector_db, chunker)


def get_chat_service() -> ChatService:
    return ChatService(
        vector_db, file_storage_adapter)
