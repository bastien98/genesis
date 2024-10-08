from dataclasses import dataclass, field
from typing import List
from file_api_v2.domain.entities.document import Document


@dataclass
class KnowledgeBase:
    kb_name: str
    docs: List[Document] = field(default_factory=list)

    def add_document(self, document: Document) -> None:
        self.docs.append(document)
        print(f"Document '{document.doc_name}' added to raw_docs in Knowledge Base '{self.kb_name}'")

    def validate_document(self, document: Document) -> None:
        # Check if a document with the same name already exists
        if any(doc.doc_name == document.doc_name for doc in self.docs):
            raise ValueError(
                f"Document with name '{document.doc_name}' already exists in Knowledge Base '{self.kb_name}'")
