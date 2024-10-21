from sqlalchemy import create_engine

from file_api_v2 import config
from file_api_v2.repositories.user_repository import UserRepository
from file_api_v2.services.kb_service import KbService
from file_api_v2.services.bm25_manager import Bm25Manager
from file_api_v2.services.document_manager import FileStore
from file_api_v2.services.retriever_service import RetrieverService
from file_api_v2.services.vector_db_manager import VectorDbService
from infra.embeddings.adapters.openai_embeddings import OpenAIEmbeddingsClient
from infra.mysql.adapters.users_adapter import UsersAdapter
from infra.storage.adapters.local_storage_adapter import LocalFileFileStorageAdapter

import json
import os
from enum import StrEnum
from file_api.core.services.embeddings_service import EmbeddingsService
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from infra.storage.adapters.local_vector_db_storage import LocalChromaDbAdapter

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

file_storage_adapter = LocalFileFileStorageAdapter()


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(EMBEDDINGS_CLIENT)


def get_document_manager() -> FileStore:
    return FileStore(LocalFileFileStorageAdapter())


engine = create_engine(config.DB_CONNECTION_STR)
users_repo = UserRepository(UsersAdapter(engine))


def get_users_repo() -> UserRepository:
    return users_repo


def get_kb_service() -> KbService:
    return KbService(users_repo)


local_vector_db_adapter = LocalChromaDbAdapter.create(EMBEDDINGS_MODEL)


def get_vector_db_manager() -> VectorDbService:
    return VectorDbService(local_vector_db_adapter)


def get_bm25_manager() -> Bm25Manager:
    return Bm25Manager(file_storage_adapter)


def get_retriever_service() -> RetrieverService:
    return RetrieverService(local_vector_db_adapter, get_document_manager())
