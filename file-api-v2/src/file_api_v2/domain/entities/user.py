from dataclasses import dataclass

from file_api_v2.domain.entities.knowledge_base import KnowledgeBase


@dataclass
class User:
    username: str
    kbs: list[KnowledgeBase]
