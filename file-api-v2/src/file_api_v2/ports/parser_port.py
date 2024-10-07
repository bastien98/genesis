from abc import ABC, abstractmethod

from file_api_v2.domain.entities.document import Document


class MarkdownParserPort(ABC):
    @abstractmethod
    async def parse_to_markdown_document(self, content: bytes, filename: str) -> Document:
        pass
