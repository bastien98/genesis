from abc import ABC, abstractmethod
from langchain_core.documents import Document

from file_api.core.ports.file_storage_port import FileLocation


class FileParserPort(ABC):
    @abstractmethod
    async def parse_to_clean_document(self, file_location: FileLocation) -> Document:
        pass
