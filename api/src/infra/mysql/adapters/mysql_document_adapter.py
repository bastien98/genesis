from sqlalchemy.orm import Session
from typing import Optional
from domain.entities.document import Document
from infra.mysql.dtos import DocumentDto
from ports.document_repository_port import DocumentRepositoryPort


class MySQLDocumentAdapter(DocumentRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def add(self, kb_id: int, document: Document) -> None:
        doc_dto = DocumentDto(name=document.name, source=document.source, kb_id=kb_id)
        self.session.add(doc_dto)
        self.session.commit()
        document.doc_id = doc_dto.doc_id

    def get_by_name(self, kb_id: int, doc_name: str) -> Optional[Document]:
        doc_dto = self.session.query(DocumentDto).filter_by(kb_id=kb_id, name=doc_name).first()
        if doc_dto is None:
            return None
        return Document(doc_id=doc_dto.doc_id, name=doc_dto.name, source=doc_dto.source)

    def get_by_id(self, doc_id: int) -> Optional[Document]:
        doc_dto = self.session.query(DocumentDto).filter_by(doc_id=doc_id).first()
        if doc_dto is None:
            return None
        return Document(doc_id=doc_dto.doc_id, name=doc_dto.name, source=doc_dto.source)

    def update(self, document: Document) -> None:
        doc_dto = self.session.query(DocumentDto).filter_by(doc_id=document.doc_id).first()
        if doc_dto is None:
            raise Exception(f"Document '{document.name}' not found")
        doc_dto.name = document.name
        doc_dto.source = document.source
        self.session.commit()

    def delete(self, document: Document) -> None:
        doc_dto = self.session.query(DocumentDto).filter_by(doc_id=document.doc_id).first()
        if doc_dto is None:
            raise Exception(f"Document '{document.name}' not found")
        self.session.delete(doc_dto)
        self.session.commit()