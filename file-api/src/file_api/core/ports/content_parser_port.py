from abc import ABC, abstractmethod
from langchain_core.documents import Document


class ContentParserPort(ABC):
    @abstractmethod
    async def parse_to_raw_document(self, content: bytes) -> Document:
        pass
