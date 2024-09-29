import json
import os
from enum import StrEnum
from file_api.adapters.embeddings.openai_embeddings import OpenAIEmbeddingsClient
from file_api.adapters.parsers.llama_parser import LlamaParser
from file_api.adapters.storage.local_file_storage_adapter import LocalFileStorageAdapter
from file_api.adapters.storage.local_vector_db_storge import LocalChromaDbAdapter
from file_api.core.domain.chunkers import HeaderChunker
from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.domain.indexing import bm25_simple
from file_api.core.services.embeddings_service import EmbeddingsService
from file_api.core.services.file_service import FileStorageService
from file_api.core.services.kb_service import KBService
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import chromadb

load_dotenv()


class Model(StrEnum):
    OPENAI = "openai"
    OLLAMA = "ollama"


# Default to OpenAI if MODEL is not defined or invalid
model_env = os.getenv('MODEL', '{"openai": "text-embedding-ada-002"}')
try:
    embeddings_model = json.loads(model_env)
except json.JSONDecodeError:
    print(f"Invalid JSON format in MODEL environment variable: {model_env}. Defaulting to OpenAI.")
    embeddings_model = {Model.OPENAI: "text-embedding-ada-002"}

# Check which model to use and set EMBEDDINGS_MODEL accordingly
if Model.OPENAI in embeddings_model:
    EMBEDDINGS_MODEL_STR = embeddings_model[Model.OPENAI]
    embeddings_client = OpenAIEmbeddingsClient(OpenAIEmbeddings(model=EMBEDDINGS_MODEL_STR))
    print(f"using the OpenAI embeddings model: {EMBEDDINGS_MODEL_STR}")
elif Model.OLLAMA in embeddings_model:
    EMBEDDINGS_MODEL_STR = embeddings_model[Model.OLLAMA]
    raise NotImplementedError("The 'embeddings_client' for Ollama embeddings is not implemented yet. Please implement "
                              "the client functionality.")
else:
    EMBEDDINGS_MODEL_STR = embeddings_model[Model.OPENAI]
    embeddings_client = OpenAIEmbeddingsClient(OpenAIEmbeddings(model=EMBEDDINGS_MODEL_STR))
    print(f"Defaulting to OpenAI embeddings model: {EMBEDDINGS_MODEL_STR}")

file_storage_adapter = LocalFileStorageAdapter()


def get_file_service() -> FileStorageService:
    return FileStorageService(file_storage_adapter, LlamaParser(), HeaderChunker())


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(embeddings_client)


vector_db = LocalChromaDbAdapter(chromadb.PersistentClient(path="../../../data/processed/vector_db"), OpenAIEmbeddings())


def get_kb_service() -> KBService:
    return KBService(file_storage_adapter, bm25_simple, vector_db)
#
