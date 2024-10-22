from dataclasses import dataclass, field
from typing import List, Optional
from file_api_v2.domain.entities.knowledge_base import KnowledgeBase


@dataclass
class User:
    username: str
    kbs: List[KnowledgeBase] = field(default_factory=list)

    def get_knowledge_base(self, kb_name: str) -> KnowledgeBase:
        """Retrieves a KnowledgeBase by its kb_name."""
        for kb in self.kbs:
            if kb.name == kb_name:
                return kb

        raise KnowledgeBaseNotFoundException(kb_name)


class KnowledgeBaseNotFoundException(Exception):
    """Exception raised when a KnowledgeBase is not found."""

    def __init__(self, kb_name: str):
        super().__init__(f"KnowledgeBase with name '{kb_name}' not found.")
        self.kb_name = kb_name
