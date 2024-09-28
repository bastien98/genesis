from abc import ABC, abstractmethod


class ContentParserPort(ABC):
    @abstractmethod
    async def parse_to_text(self, content: bytes) -> str:
        pass
