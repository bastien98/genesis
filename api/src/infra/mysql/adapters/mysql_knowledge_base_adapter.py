from sqlalchemy.orm import Session
from typing import Optional
from domain.entities.knowledge_base import KnowledgeBase
from domain.entities.document import Document
from infra.mysql.dtos import KnowledgeBaseDTO
from ports.knowledge_base_repository_port import KnowledgeBaseRepositoryPort


class MySQLKbAdapter(KnowledgeBaseRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_id: int, knowledge_base: KnowledgeBase) -> None:
        kb_dto = KnowledgeBaseDTO(name=knowledge_base.name, user_id=user_id)
        self.session.add(kb_dto)
        self.session.commit()
        knowledge_base.kb_id = kb_dto.kb_id

    def get_by_name(self, user_id: int, kb_name: str) -> Optional[KnowledgeBase]:
        kb_dto = self.session.query(KnowledgeBaseDTO).filter_by(user_id=user_id, name=kb_name).first()
        if kb_dto is None:
            return None
        return self._dto_to_entity(kb_dto)

    def get_by_id(self, kb_id: int) -> Optional[KnowledgeBase]:
        kb_dto = self.session.query(KnowledgeBaseDTO).filter_by(kb_id=kb_id).first()
        if kb_dto is None:
            return None
        return self._dto_to_entity(kb_dto)

    def update(self, knowledge_base: KnowledgeBase) -> None:
        kb_dto = self.session.query(KnowledgeBaseDTO).filter_by(kb_id=knowledge_base.kb_id).first()
        if kb_dto is None:
            raise Exception(f"KnowledgeBase '{knowledge_base.name}' not found")
        kb_dto.name = knowledge_base.name
        self.session.commit()

    def delete(self, knowledge_base: KnowledgeBase) -> None:
        kb_dto = self.session.query(KnowledgeBaseDTO).filter_by(kb_id=knowledge_base.kb_id).first()
        if kb_dto is None:
            raise Exception(f"KnowledgeBase '{knowledge_base.name}' not found")
        self.session.delete(kb_dto)
        self.session.commit()

    def _dto_to_entity(self, kb_dto: KnowledgeBaseDTO) -> KnowledgeBase:
        documents = []
        for doc_dto in kb_dto.docs:
            document = Document(doc_id=doc_dto.doc_id, name=doc_dto.name, source=doc_dto.source)
            documents.append(document)
        kb = KnowledgeBase(kb_id=kb_dto.kb_id, name=kb_dto.name, documents=documents)
        return kb
