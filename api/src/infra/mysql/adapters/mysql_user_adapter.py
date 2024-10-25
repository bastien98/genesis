from sqlalchemy.orm import Session
from typing import Optional
from domain.entities.user import User, KnowledgeBase
from domain.entities.document import Document
from infra.mysql.dtos import UserDTO
from ports.user_repository_port import UserRepositoryPort


class MySQLUserAdapter(UserRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user: User) -> None:
        user_dto = UserDTO(username=user.username)
        self.session.add(user_dto)
        self.session.commit()
        user.user_id = user_dto.user_id

    def get_by_username(self, username: str) -> Optional[User]:
        user_dto = self.session.query(UserDTO).filter_by(username=username).first()
        if user_dto is None:
            return None
        knowledge_bases = []
        for kb_dto in user_dto.kbs:
            documents = []
            for doc_dto in kb_dto.docs:
                document = Document(doc_id=doc_dto.doc_id, name=doc_dto.name, source=doc_dto.source)
                documents.append(document)
            kb = KnowledgeBase(kb_id=kb_dto.kb_id, name=kb_dto.name, documents=documents)
            knowledge_bases.append(kb)
        user = User(user_id=user_dto.user_id, username=user_dto.username, knowledge_bases=knowledge_bases)
        return user

    def get_by_user_id(self, user_id: int) -> Optional[User]:
        user_dto = self.session.query(UserDTO).filter_by(user_id=user_id).first()
        if user_dto is None:
            return None
        knowledge_bases = []
        for kb_dto in user_dto.kbs:
            documents = []
            for doc_dto in kb_dto.docs:
                document = Document(doc_id=doc_dto.doc_id, name=doc_dto.name, source=doc_dto.source)
                documents.append(document)
            kb = KnowledgeBase(kb_id=kb_dto.kb_id, name=kb_dto.name, documents=documents)
            knowledge_bases.append(kb)
        user = User(user_id=user_dto.user_id, username=user_dto.username, knowledge_bases=knowledge_bases)
        return user

    def update(self, user: User) -> None:
        user_dto = self.session.query(UserDTO).filter_by(user_id=user.user_id).first()
        if user_dto is None:
            raise Exception(f"User '{user.username}' not found")
        user_dto.username = user.username
        self.session.commit()

    def delete(self, user: User) -> None:
        user_dto = self.session.query(UserDTO).filter_by(user_id=user.user_id).first()
        if user_dto is None:
            raise Exception(f"User '{user.username}' not found")
        self.session.delete(user_dto)
        self.session.commit()
