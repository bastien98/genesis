from dataclasses import dataclass, field
from typing import List


@dataclass
class RawDocument:
    name: str
    source: str
    content: bytes


@dataclass
class Document:
    name: str
    source: str


@dataclass
class KnowledgeBase:
    name: str
    documents: List[Document] = field(default_factory=list)



@dataclass
class User:
    username: str
    knowledge_bases: List[KnowledgeBase] = None

    def get_knowledge_base_by_name(self, kb_name: str) -> KnowledgeBase:
        for kb in self.knowledge_bases:
            if kb.name == kb_name:
                return kb
        raise KnowledgeBaseNotFoundError(self.username, kb_name)

    def add_document_to_knowledge_base(self, kb_name: str, document: Document) -> None:
        kb = self.get_knowledge_base_by_name(kb_name)
        kb.documents.append(document)


class KnowledgeBaseNotFoundError(Exception):
    def __init__(self, username: str, kb_name: str):
        super().__init__(f"Knowledge base '{kb_name}' not found for user '{username}'.")
