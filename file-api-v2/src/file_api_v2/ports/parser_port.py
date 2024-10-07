from abc import ABC, abstractmethod


class MarkdownParserPort(ABC):
    @abstractmethod
    async def parse_to_markdown_chunks(self, content: bytes, filename: str) -> list[str]:
        pass


class TextParserPort(ABC):
    @abstractmethod
    async def parse_to_text_chunks(self, content: bytes) -> list[str]:
        pass
