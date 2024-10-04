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
            if kb.kb_name == kb_name:
                return kb
