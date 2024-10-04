from sqlalchemy import create_engine

from file_api_v2 import config
from file_api_v2.repositories.users_repository import UsersRepository
from file_api_v2.services.KbService import KbService
from file_api_v2.services.document_manager import AbstractDocumentManager, LocalFileSystemDocumentManager
from infra.mysql.adapters.user_adapter import UsersAdapter
from infra.storage.adapters.local_storage_adapter import LocalFileStorageAdapter


def get_document_manager() -> AbstractDocumentManager:
    return LocalFileSystemDocumentManager(LocalFileStorageAdapter())


def get_kb_service() -> KbService:
    engine = create_engine(config.DB_CONNECTION_STR)
    return KbService(UsersRepository(UsersAdapter(engine)))
