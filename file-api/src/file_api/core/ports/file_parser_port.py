from abc import ABC, abstractmethod
from langchain_core.documents import Document


class MarkdownParserPort(ABC):
    @abstractmethod
    async def parse_to_markdown_document(self, content: bytes, filename: str) -> Document:
        pass


class TextParserPort(ABC):

    @abstractmethod
    async def parse_to_text_document(self, content: bytes) -> Document:
        pass
