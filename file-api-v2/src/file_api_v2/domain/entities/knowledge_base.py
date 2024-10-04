from dataclasses import dataclass

from file_api_v2.domain.entities.documents import PdfDocument


@dataclass
class KnowledgeBase:
    kb_name: str
    docs: list[PdfDocument]

