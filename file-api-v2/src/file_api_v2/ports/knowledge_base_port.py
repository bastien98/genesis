from abc import ABC, abstractmethod

from file_api_v2.domain.entities.KnowledgeBase import KnowledgeBase


class KnowledgeBasePort(ABC):

    @abstractmethod
    def retrieve_knowledge_base_for_user(self, user_id: int, kb_id: int) -> KnowledgeBase:
        pass
