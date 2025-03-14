from anthropic import AsyncAnthropic
from fastapi import Depends
from instructor import AsyncInstructor, patch, Mode
from ollama import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infra.mysql.adapters.mysql_chat_adapter import MySQLChatAdapter
from infra.mysql.adapters.mysql_document_adapter import MySQLDocumentAdapter
from infra.mysql.adapters.mysql_knowledge_base_adapter import MySQLKbAdapter
from infra.mysql.adapters.mysql_user_adapter import MySQLUserAdapter
from infra.context.adapters.ollama_context_generator import OllamaContextAdapter
from infra.context.adapters.anthropic_context_adapter import AnthropicContextAdapter
from infra.storage.adapters.local_location_adapter import LocalLocationAdapter
from ports.context_generator_port import ContextGeneratorPort
from ports.document_repository_port import DocumentRepositoryPort
from ports.knowledge_base_repository_port import KnowledgeBaseRepositoryPort
from ports.user_repository_port import UserRepositoryPort
from repositories.document_repository import DocumentRepository
from repositories.knowledge_base_repository import KnowledgeBaseRepository
from repositories.user_repository import UserRepository
from services.chat_service import ChatService
from services.context_service import ContextService
from services.file_storage_service import FileStorageService
from services.bm25_service import Bm25Service
from services.knowledge_base_service import KnowledgeBaseService
from services.location_service import LocationService
from services.retriever_service import RetrieverService
from services.vector_db_service import VectorDbService
from utils.parser import Parser
from infra.embeddings.adapters.openai_embeddings import OpenAIEmbeddingsClient
from infra.storage.adapters.local_storage_adapter import LocalFileStorageAdapter
import json
import os
from enum import StrEnum
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
from infra.storage.adapters.local_vector_db_adapter import LocalChromaDbAdapter

load_dotenv()


class Model(StrEnum):
    OPENAI = "openai"
    OLLAMA = "ollama"


# Default to OpenAI if MODEL is not defined or invalid
default_model = {"publisher": "openai", "embeddings": "text-embedding-ada-002", "model": "gpt-4o"}
model_env = os.getenv('MODEL', default_model)
try:
    model_conf = json.loads(model_env)
except json.JSONDecodeError:
    print(f"Invalid JSON format in MODEL environment variable: {model_env}. Defaulting to OpenAI.")
    model_conf = default_model

# Check which model to use and set EMBEDDINGS_MODEL accordingly
if Model.OPENAI == model_conf.get("publisher"):
    EMBEDDINGS_MODEL = OpenAIEmbeddings(model=model_conf.get("embeddings"))
    EMBEDDINGS_CLIENT = OpenAIEmbeddingsClient(EMBEDDINGS_MODEL)
    LLM = ChatOpenAI(model=model_conf.get("model"))
    print(f"using the OpenAI model with conf: {model_conf}")
elif Model.OLLAMA in model_conf:
    EMBEDDINGS_MODEL = OllamaEmbeddings(model=model_conf[Model.OLLAMA])
    raise NotImplementedError("The 'embeddings_client' for Ollama embeddings is not implemented yet. Please implement "
                              "the client functionality.")
else:
    EMBEDDINGS_MODEL = OpenAIEmbeddings(model=model_conf[Model.OPENAI])
    EMBEDDINGS_CLIENT = OpenAIEmbeddingsClient(EMBEDDINGS_MODEL)
    print(
        f"Environment variable MODEL undefined, defaulting to OpenAI embeddings model: {model_conf[Model.OPENAI]}")


def get_local_location_adapter():
    return LocalLocationAdapter()


def get_location_service(
        adapter: LocalLocationAdapter = Depends(get_local_location_adapter)
) -> LocationService:
    return LocationService(adapter)


def get_local_file_storage_adapter():
    return LocalFileStorageAdapter()


def get_local_vector_db_adapter():
    return LocalChromaDbAdapter.create(EMBEDDINGS_MODEL)


# Create session to database
Session = sessionmaker(bind=create_engine(os.getenv("DB_CONN")))
session = Session()


def get_document_adapter() -> DocumentRepositoryPort:
    return MySQLDocumentAdapter(session)


def get_knowledge_base_adapter() -> KnowledgeBaseRepositoryPort:
    return MySQLKbAdapter(session)


def get_user_adapter() -> UserRepositoryPort:
    return MySQLUserAdapter(session)


# def get_user_adapter():
#     return UsersAdapter(create_engine(os.getenv("DB_CONN")))


def get_file_storage_service(
        adapter: LocalFileStorageAdapter = Depends(get_local_file_storage_adapter)
):
    return FileStorageService(adapter)


def get_vector_db_service(
        adapter: LocalChromaDbAdapter = Depends(get_local_vector_db_adapter)
):
    return VectorDbService(adapter)


# def get_user_repository(
#         adapter: UsersAdapter = Depends(get_user_adapter)
# ):
#     return UserRepository(adapter)

def get_document_repository(
        adapter: DocumentRepositoryPort = Depends(get_document_adapter)
):
    return DocumentRepository(adapter)


def get_knowledge_base_repository(
        adapter: KnowledgeBaseRepositoryPort = Depends(get_knowledge_base_adapter)
):
    return KnowledgeBaseRepository(adapter)


def get_user_repository(
        adapter: UserRepositoryPort = Depends(get_user_adapter)
):
    return UserRepository(adapter)


def get_parser():
    return Parser()


def get_ollama_context_generator_adapter():
    return OllamaContextAdapter(client=AsyncClient())


def get_anthropic_context_generator_adapter():
    return AnthropicContextAdapter(client=AsyncInstructor(
        client=AsyncAnthropic(),
        create=patch(
            create=AsyncAnthropic().beta.prompt_caching.messages.create,
            mode=Mode.ANTHROPIC_TOOLS,
        ),
        mode=Mode.ANTHROPIC_TOOLS,
    ))


def get_context_service(
        adapter: ContextGeneratorPort = Depends(get_anthropic_context_generator_adapter)
):
    return ContextService(adapter)


def get_bm25_service(
        location_service: LocationService = Depends(get_location_service),
        file_storage_service: FileStorageService = Depends(get_file_storage_service)
):
    return Bm25Service(location_service, file_storage_service)


def get_retriever_service(
        location_service: LocationService = Depends(get_location_service),
        kb_repo: KnowledgeBaseRepository = Depends(get_knowledge_base_repository),
        vectordb_service: VectorDbService = Depends(get_vector_db_service),
        file_storage_service: FileStorageService = Depends(get_file_storage_service)
):
    return RetrieverService(location_service, kb_repo, vectordb_service, file_storage_service)


def get_knowledge_base_service(
        file_storage_service: FileStorageService = Depends(get_file_storage_service),
        vector_db_service: VectorDbService = Depends(get_vector_db_service),
        user_repository: UserRepository = Depends(get_user_repository),
        parser: Parser = Depends(get_parser),
        context_service: ContextService = Depends(get_context_service),
        location_service=Depends(get_location_service),
        bm25_service: Bm25Service = Depends(get_bm25_service),
        kb_repo: KnowledgeBaseRepository = Depends(get_knowledge_base_repository),
        document_repo: DocumentRepository = Depends(get_document_repository),
        retriever_service: RetrieverService = Depends(get_retriever_service)
) -> KnowledgeBaseService:
    return KnowledgeBaseService(
        file_storage_service,
        vector_db_service,
        parser,
        context_service,
        location_service,
        bm25_service,
        user_repository,
        kb_repo,
        document_repo,
        retriever_service
    )


def get_chat_service() -> ChatService:
    return ChatService(MySQLChatAdapter(session))
