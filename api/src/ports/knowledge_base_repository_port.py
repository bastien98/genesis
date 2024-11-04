from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.knowledge_base import KnowledgeBase


class KnowledgeBaseRepositoryPort(ABC):
    @abstractmethod
    def add(self, user_id: int, knowledge_base: KnowledgeBase) -> None:
        pass

    @abstractmethod
    def get_by_name(self, user_id: int, kb_name: str) -> Optional[KnowledgeBase]:
        pass

    @abstractmethod
    def get_by_id(self, kb_id: int) -> Optional[KnowledgeBase]:
        pass

    @abstractmethod
    def update(self, knowledge_base: KnowledgeBase) -> None:
        pass

    @abstractmethod
    def delete(self, kb_id: int) -> None:
        pass

    @abstractmethod
    def get_all_kb_for_user(self, kb_id: int) -> Optional[List[KnowledgeBase]]:
        pass
