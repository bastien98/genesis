from typing import Optional
from domain.entities.document import Document
from ports.document_repository_port import DocumentRepositoryPort


class DocumentRepository:
    def __init__(self, document_repo_adapter: DocumentRepositoryPort):
        self.document_repo_adapter = document_repo_adapter

    def add(self, kb_id: int, document: Document) -> None:
        self.document_repo_adapter.add(kb_id, document)

    def get_by_name(self, kb_id: int, doc_name: str) -> Optional[Document]:
        return self.document_repo_adapter.get_by_name(kb_id, doc_name)

    def get_by_id(self, doc_id: int) -> Optional[Document]:
        return self.document_repo_adapter.get_by_id(doc_id)

    def update(self, document: Document) -> None:
        self.document_repo_adapter.update(document)

    def delete(self, doc_id: int) -> None:
        self.document_repo_adapter.delete(doc_id)
