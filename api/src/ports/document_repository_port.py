from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.document import Document


class DocumentRepositoryPort(ABC):
    @abstractmethod
    def add(self, kb_id: int, document: Document) -> None:
        pass

    @abstractmethod
    def get_by_name(self, kb_id: int, doc_name: str) -> Optional[Document]:
        pass

    @abstractmethod
    def get_by_id(self, doc_id: int) -> Optional[Document]:
        pass

    @abstractmethod
    def update(self, document: Document) -> None:
        pass

    @abstractmethod
    def delete(self, doc_id: int) -> None:
        pass
