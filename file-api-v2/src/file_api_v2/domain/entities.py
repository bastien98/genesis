from dataclasses import dataclass
from enum import Enum
from typing import List

from rank_bm25 import BM25Okapi


class ContentType(Enum):
    TEXT = "text"
    MARKDOWN = "markdown"


@dataclass
class RawDocument:
    name: str
    source: str
    content: bytes


@dataclass
class Document:
    name: str
    source: str
    raw_doc_path: str
    text_chunks_doc_path: str
    md_chunks_doc_path: str


@dataclass
class Chunk:
    index: int
    text_content: str
    md_content: str


@dataclass
class BM25Index:
    index_data: BM25Okapi


@dataclass
class KnowledgeBase:
    name: str
    documents: List[Document] = None
    bm25_index: BM25Index = None


@dataclass
class User:
    username: str
    knowledge_bases: List[KnowledgeBase] = None
