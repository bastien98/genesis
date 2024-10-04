from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from file_api_v2.domain.entities.documents import PdfDocument
from file_api_v2.domain.entities.knowledge_base import KnowledgeBase
from file_api_v2.domain.entities.user import User
from file_api_v2.ports.user_port import UsersPort
from infra.mysql.dtos import UserDTO, KnowledgeBaseDTO, PdfDocumentDTO


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

    def update_user(self, user: User) -> None:
        """Update an existing User domain object in the database."""
        with Session(bind=self.db_engine) as session:
            # Check if the user exists
            existing_user = session.query(UserDTO).filter(UserDTO.username == user.username).one_or_none()

            if not existing_user:
                # Raise a custom exception if the user does not exist
                raise UserNotFoundException

            existing_kbs_dict = {kb.kb_name: kb for kb in existing_user.kbs}

            # Iterate over the user's knowledge bases from the domain model
            for kb in user.kbs:
                if kb.kb_name in existing_kbs_dict:
                    # Update existing knowledge base
                    kb_dto = existing_kbs_dict[kb.kb_name]
                    kb_dto.kb_name = kb.kb_name  # Update any other fields if necessary

                    # Create a dictionary for existing documents within this KB
                    existing_docs_dict = {doc.document_name: doc for doc in kb_dto.docs}

                    # Update existing documents or add new ones
                    for doc in kb.docs:
                        if doc.doc_name in existing_docs_dict:
                            # Update the existing document
                            doc_dto = existing_docs_dict[doc.doc_name]
                            doc_dto.source = doc.source
                            doc_dto.doc_path = doc.doc_path
                        else:
                            # Insert new document
                            doc_dto = PdfDocumentDTO(
                                document_name=doc.doc_name,
                                source=doc.source,
                                doc_path=doc.doc_path,
                            )
                            kb_dto.docs.append(doc_dto)

            session.commit()


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
