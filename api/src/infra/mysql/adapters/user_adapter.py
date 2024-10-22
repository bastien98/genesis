import logging
from sqlalchemy import Engine
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session, joinedload

from domain.entities.document import Document
from domain.entities.knowledge_base import KnowledgeBase
from domain.entities.user import User
from ports.user_port import UsersPort
from infra.mysql.dtos import UserDTO, KnowledgeBaseDTO, DocumentDto

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set this to INFO or WARNING in production


class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the database."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' was not found.")


class UsersAdapter(UsersPort):
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine
        logger.debug("UsersAdapter initialized with db_engine: %s", db_engine)

    def retrieve_user(self, username: str) -> User:
        logger.debug("Attempting to retrieve user: %s", username)
        with Session(bind=self.db_engine) as session:
            try:
                # Query UserDTO with eager loading of knowledge bases and documents
                user_dto = (
                    session.query(UserDTO)
                    .options(
                        joinedload(UserDTO.kbs).joinedload(KnowledgeBaseDTO.docs)
                    )
                    .filter(UserDTO.username == username)
                    .one()
                )
                logger.debug("UserDTO retrieved: %s", user_dto)
            except NoResultFound:
                logger.error("UserNotFoundException: User '%s' not found.", username)
                raise UserNotFoundException(username)

            user = self._map_user_dto_to_domain(user_dto)
            logger.debug("Mapped User domain object: %s", user)
            return user

    def update_user(self, user: User) -> None:
        logger.debug("Attempting to update user: %s", user.username)
        with Session(bind=self.db_engine) as session:
            # Retrieve the existing user DTO
            existing_user = (
                session.query(UserDTO)
                .options(
                    joinedload(UserDTO.kbs).joinedload(KnowledgeBaseDTO.docs)
                )
                .filter(UserDTO.username == user.username)
                .one_or_none()
            )

            if not existing_user:
                logger.error("UserNotFoundException: User '%s' not found.", user.username)
                raise UserNotFoundException(user.username)

            # Update the existing user DTO with the domain model
            self._update_user_dto(existing_user, user, session)
            logger.debug("UserDTO after update: %s", existing_user)

            try:
                session.commit()
                logger.info("User '%s' updated successfully.", user.username)
            except Exception as e:
                session.rollback()
                logger.exception("Exception occurred while updating user '%s': %s", user.username, e)
                raise

    def _update_user_dto(self, user_dto: UserDTO, user: User, session):
        """Update UserDTO fields and related knowledge bases."""
        logger.debug("Updating UserDTO: %s", user_dto.username)

        # Update simple fields if there are any (e.g., email)
        # user_dto.email = user.email  # Uncomment if email field exists

        # Create a dictionary of existing knowledge bases keyed by kb_name
        existing_kbs_dict = {kb_dto.name: kb_dto for kb_dto in user_dto.kbs}

        logger.debug("Existing KnowledgeBases: %s", list(existing_kbs_dict.keys()))

        # Keep track of knowledge bases to remove
        kbs_to_remove = set(existing_kbs_dict.keys())

        for kb in user.knowledge_bases:
            logger.debug("Processing KnowledgeBase: %s", kb.name)
            kbs_to_remove.discard(kb.name)
            if kb.name in existing_kbs_dict:
                # Update existing knowledge base
                kb_dto = existing_kbs_dict[kb.name]
                logger.info("Updating existing KnowledgeBaseDTO: %s", kb_dto.name)
                self._update_kb_dto(kb_dto, kb, session)
            else:
                # Add new knowledge base
                kb_dto = KnowledgeBaseDTO(name=kb.name, user_id=user_dto.user_id)
                user_dto.kbs.append(kb_dto)
                logger.info("Added new KnowledgeBaseDTO: %s", kb_dto.name)
                self._update_kb_dto(kb_dto, kb, session)

        # Remove knowledge bases not present in the domain model
        for kb_name in kbs_to_remove:
            kb_dto = existing_kbs_dict[kb_name]
            logger.debug("Removing KnowledgeBaseDTO: %s", kb_dto.name)
            user_dto.kbs.remove(kb_dto)
            session.delete(kb_dto)

    def _update_kb_dto(self, kb_dto: KnowledgeBaseDTO, kb: KnowledgeBase, session):
        """Update KnowledgeBaseDTO fields and related documents."""
        logger.debug("Updating KnowledgeBaseDTO: %s", kb_dto.name)

        # Update simple fields if there are any

        # Create a dictionary of existing documents keyed by document name
        existing_docs_dict = {doc_dto.name: doc_dto for doc_dto in kb_dto.docs}
        logger.debug("Existing Documents: %s", list(existing_docs_dict.keys()))

        # Keep track of documents to remove
        docs_to_remove = set(existing_docs_dict.keys())

        for doc in kb.documents:
            logger.debug("Processing Document: %s", doc.name)
            docs_to_remove.discard(doc.name)
            if doc.name in existing_docs_dict:
                # Update existing document
                doc_dto = existing_docs_dict[doc.name]
                logger.debug("Updating existing DocumentDto: %s", doc_dto.name)
                self._update_doc_dto(doc_dto, doc)
            else:
                # Add new document
                doc_dto = DocumentDto(
                    name=doc.name,
                    kb_id=kb_dto.kb_id,
                    source=doc.source
                )
                kb_dto.docs.append(doc_dto)
                logger.debug("Added new DocumentDto: %s", doc_dto.name)

        # Remove documents not present in the domain model
        for doc_name in docs_to_remove:
            doc_dto = existing_docs_dict[doc_name]
            logger.debug("Removing DocumentDto: %s", doc_dto.name)
            kb_dto.docs.remove(doc_dto)
            session.delete(doc_dto)

    def _update_doc_dto(self, doc_dto: DocumentDto, doc: Document):
        """Update DocumentDto fields."""
        logger.debug("Updating DocumentDto: %s", doc_dto.name)
        doc_dto.source = doc.source
        # Update other fields if necessary

    def _map_user_dto_to_domain(self, user_dto: UserDTO) -> User:
        """Map UserDTO to User domain model."""
        logger.debug("Mapping UserDTO to User domain model for user: %s", user_dto.username)
        return User(
            username=user_dto.username,
            knowledge_bases=[
                KnowledgeBase(
                    name=kb.name,
                    documents=[
                        Document(
                            name=doc.name,
                            source=doc.source,
                        )
                        for doc in kb.docs
                    ]
                )
                for kb in user_dto.kbs
            ]
        )