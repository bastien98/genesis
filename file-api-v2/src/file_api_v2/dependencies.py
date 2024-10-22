from fastapi import Depends
from sqlalchemy import create_engine

from file_api_v2 import config
from file_api_v2.repositories.user_repository import UserRepository
from file_api_v2.services.context_service import ContextService
from file_api_v2.services.file_storage_service import FileStorageService
from file_api_v2.services.kb_service import KbService
from file_api_v2.services.bm25_service import Bm25Service
from file_api_v2.services.document_manager import FileStore
from file_api_v2.services.knowledge_base_service import KnowledgeBaseService
from file_api_v2.services.location_service import LocalLocationService
from file_api_v2.services.retriever_service import RetrieverService
from file_api_v2.services.vector_db_service import VectorDbService
from file_api_v2.utils.parser import Parser
from infra.embeddings.adapters.openai_embeddings import OpenAIEmbeddingsClient
from infra.mysql.adapters.users_adapter import UsersAdapter
from infra.storage.adapters.local_storage_adapter import LocalFileStorageAdapter

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

file_storage_adapter = LocalFileStorageAdapter()


def get_embeddings_service() -> EmbeddingsService:
    return EmbeddingsService(EMBEDDINGS_CLIENT)


def get_document_manager() -> FileStore:
    return FileStore(LocalFileStorageAdapter())


def get_users_repo() -> UserRepository:
    return users_repo


def get_kb_service() -> KbService:
    return KbService(users_repo)


def get_vector_db_manager() -> VectorDbService:
    return VectorDbService(local_vector_db_adapter)


def get_bm25_manager() -> Bm25Service:
    return Bm25Service(file_storage_adapter)


def get_retriever_service() -> RetrieverService:
    return RetrieverService(local_vector_db_adapter, get_document_manager())






def get_location_service() -> LocalLocationService:
    return LocalLocationService()


def get_local_file_storage_adapter():
    return LocalFileStorageAdapter()


def get_local_vector_db_adapter():
    return LocalChromaDbAdapter.create(EMBEDDINGS_MODEL)


def get_user_adapter():
    return UsersAdapter(create_engine(config.DB_CONNECTION_STR))


def get_file_storage_service(
        adapter: LocalFileStorageAdapter = Depends(get_local_file_storage_adapter)
):
    return FileStorageService(adapter)


def get_vector_db_service(
        adapter: LocalChromaDbAdapter = Depends(get_local_vector_db_adapter)
):
    return VectorDbService(adapter)


def get_user_repository(
        adapter: UsersAdapter = Depends(get_user_adapter)
):
    return UserRepository(adapter)


def get_parser():
    return Parser()


def get_context_service():
    return ContextService()


def get_bm25_service(
        location_service=Depends(get_location_service),
        adapter: LocalFileStorageAdapter = Depends(get_local_file_storage_adapter)
):
    return Bm25Service(location_service, adapter)


def get_knowledge_base_service(
        file_storage_service: FileStorageService = Depends(get_file_storage_service),
        vector_db_service: VectorDbService = Depends(get_vector_db_service),
        user_repository: UserRepository = Depends(get_user_repository),
        parser: Parser = Depends(get_parser),
        context_service: ContextService = Depends(get_context_service),
        location_service=Depends(get_location_service),
        bm25_service: Bm25Service = Depends(get_bm25_service),
) -> KnowledgeBaseService:
    return KnowledgeBaseService(
        file_storage_service,
        vector_db_service,
        user_repository,
        parser,
        context_service,
        location_service,
        bm25_service
    )
