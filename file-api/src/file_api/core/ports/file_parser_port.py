from abc import ABC, abstractmethod
from langchain_core.documents import Document


class FileParserPort(ABC):
    @abstractmethod
    async def parse_to_clean_document(self, content: bytes, filename: str) -> Document:
        pass
