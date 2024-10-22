from fastapi import Depends
from sqlalchemy import create_engine
from repositories.user_repository import UserRepository
from services.context_service import ContextService
from services.file_storage_service import FileStorageService
from services.bm25_service import Bm25Service
from services.knowledge_base_service import KnowledgeBaseService
from services.location_service import LocalLocationService
from services.vector_db_service import VectorDbService
from utils.parser import Parser
from infra.embeddings.adapters.openai_embeddings import OpenAIEmbeddingsClient
from infra.mysql.adapters.user_adapter import UsersAdapter
from infra.storage.adapters.local_storage_adapter import LocalFileStorageAdapter
import json
import os
from enum import StrEnum
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from infra.storage.adapters.local_vector_db_adapter import LocalChromaDbAdapter

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


def get_location_service() -> LocalLocationService:
    return LocalLocationService()


def get_local_file_storage_adapter():
    return LocalFileStorageAdapter()


def get_local_vector_db_adapter():
    return LocalChromaDbAdapter.create(EMBEDDINGS_MODEL)


def get_user_adapter():
    return UsersAdapter(create_engine(os.getenv("DB_CONN")))


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
