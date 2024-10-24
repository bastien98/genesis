from typing import List
from domain.entities.document import Document
from domain.entities.knowledge_base import KnowledgeBase


class User:
    def __init__(self, user_id: int, username: str, knowledge_bases: List[KnowledgeBase] = None):
        self.user_id = user_id
        self.username = username
        self.knowledge_bases = knowledge_bases if knowledge_bases is not None else []

    def get_knowledge_base_by_name(self, kb_name: str) -> KnowledgeBase:
        """Retrieve a knowledge base by its name, or raise an exception if not found."""
        for kb in self.knowledge_bases:
            if kb.name == kb_name:
                return kb
        raise KnowledgeBaseNotFoundError(self.username, kb_name)

    def get_knowledge_base_by_id(self, kb_id: int) -> KnowledgeBase:
        for kb in self.knowledge_bases:
            if kb.kb_id == kb_id:
                return kb
        raise KnowledgeBaseNotFoundError(self.username, f"ID {kb_id}")

    def add_document_to_knowledge_base_by_name(self, kb_name: str, document: Document) -> None:
        """Add a document to the specified knowledge base."""
        kb = self.get_knowledge_base_by_name(kb_name)
        kb.add_document(document)  # Delegate to KnowledgeBase for existence check

    def add_document_to_knowledge_base_by_id(self, kb_id: int, document: Document) -> None:
        """Add a document to the specified knowledge base."""
        kb = self.get_knowledge_base_by_id(kb_id)
        kb.add_document(document)  # Delegate to KnowledgeBase for existence check


class KnowledgeBaseNotFoundError(Exception):
    def __init__(self, username: str, kb_name: str):
        super().__init__(f"Knowledge base '{kb_name}' not found for user '{username}'.")