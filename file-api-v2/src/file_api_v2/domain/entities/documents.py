from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path

from file_api_v2.utills.document_manager import AbstractDocumentManager


@dataclass
class AbstractDocument(ABC):
    user_id: str
    kb_id: str
    doc_id: str
    source: str
    document_manager: 'AbstractDocumentManager'
    raw_location: Path = field(init=False)  # This will be set in the subclasses
    chunks_location: Path = field(init=False)  # This will be set in the subclasses
    content: bytes


@dataclass
class PdfDocument(AbstractDocument):
    def __post_init__(self):
        self.raw_location = self.document_manager.get_raw_pdf_path(self.user_id, self.kb_id, self.doc_id)
        self.chunks_location = self.document_manager.get_chunked_pdf_path(self.user_id, self.kb_id, self.doc_id)