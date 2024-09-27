from abc import ABC, abstractmethod
from langchain_core.documents import Document

from file_api.core.ports.file_storage_port import FileLocation


class FileParserPort(ABC):
    @abstractmethod
    async def parse_to_clean_document(self, content: bytes, filename: str) -> Document:
        pass
