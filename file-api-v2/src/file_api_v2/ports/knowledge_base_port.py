from abc import ABC, abstractmethod


class KnowledgeBasePort(ABC):

    @abstractmethod
    def retrieve_knowledge_base(self, user_id:str, kb_id: str):
        pass
