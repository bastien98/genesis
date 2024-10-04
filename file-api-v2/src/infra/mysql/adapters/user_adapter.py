from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from file_api_v2.domain.entities.documents import PdfDocument
from file_api_v2.domain.entities.knowledge_base import KnowledgeBase
from file_api_v2.domain.entities.user import User
from file_api_v2.ports.user_port import UsersPort
from infra.mysql.dtos import UserDTO, KnowledgeBaseDTO


class UsersAdapter(UsersPort):
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def retrieve_user(self, username: str) -> User:
        with Session(bind=self.db_engine) as session:
            try:
                # Query UserDTO with eager loading of knowledge bases and documents
                user_dto = (
                    session.query(UserDTO)
                    .options(
                        joinedload(UserDTO.kbs).joinedload(KnowledgeBaseDTO.docs)  # Eager load kbs and their docs
                    )
                    .filter(UserDTO.username == username)
                    .one()  # Raises NoResultFound if no user is found
                )
            except NoResultFound:
                raise UserNotFoundException

            return map_user_dto_to_domain(user_dto)


def map_user_dto_to_domain(user_dto: UserDTO) -> User:
    return User(
        username=user_dto.username,
        kbs=[
            KnowledgeBase(
                kb_name=kb.kb_name,
                docs=[
                    PdfDocument(
                        doc_name=doc.document_name,
                        source=doc.source,
                        doc_path=doc.doc_path
                    )
                    for doc in kb.docs
                ]
            )
            for kb in user_dto.kbs
        ]
    )


class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' was not found.")
