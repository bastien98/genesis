from dataclasses import dataclass
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
    documents: List[Document] = None


@dataclass
class User:
    username: str
    knowledge_bases: List[KnowledgeBase] = None
