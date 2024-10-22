from typing import List
from domain.entities.document import Document


class KnowledgeBase:
    def __init__(self, name: str, documents: List[Document] = None):
        self.name = name
        self.documents = documents if documents is not None else []

    def document_exists(self, doc_name: str) -> bool:
        """Business rule: Check if a document with the same name already exists."""
        return any(doc.name == doc_name for doc in self.documents)

    def add_document(self, document: Document) -> None:
        """Business rule: Add document to knowledge base, ensuring no duplicates."""
        # if self.document_exists(document.name):
        #     raise DocumentAlreadyExistsError(document.name, self.name)
        self.documents.append(document)


class DocumentAlreadyExistsError(Exception):
    def __init__(self, doc_name: str, kb_name: str):
        super().__init__(f"The document '{doc_name}' already exists in the knowledge base '{kb_name}'.")
