from typing import Optional
from domain.entities.knowledge_base import KnowledgeBase
from ports.knowledge_base_repository_port import KnowledgeBaseRepositoryPort


class KnowledgeBaseRepository:
    def __init__(self, kb_repo_adapter: KnowledgeBaseRepositoryPort):
        self.kb_repo_adapter = kb_repo_adapter

    def get_by_name(self, user_id: int, kb_name: str) -> Optional[KnowledgeBase]:
        return self.kb_repo_adapter.get_by_name(user_id, kb_name)

    def get_by_id(self, kb_id: int) -> Optional[KnowledgeBase]:
        return self.kb_repo_adapter.get_by_id(kb_id)

    def update(self, knowledge_base: KnowledgeBase) -> None:
        self.kb_repo_adapter.update(knowledge_base)

    def delete(self, kb_id: int) -> None:
        self.kb_repo_adapter.delete(kb_id)

    def list_kbs_for_user(self, user_id: int) ->  list[KnowledgeBase]:
        return self.kb_repo_adapter.get_all_kb_for_user(user_id)
