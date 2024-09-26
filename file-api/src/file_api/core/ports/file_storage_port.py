from abc import ABC, abstractmethod

from file_api.core.domain.ex_document import ExDocument


class FileStoragePort(ABC):
    @abstractmethod
    async def save_document_to_raw(self, file: ExDocument) -> str:
        pass
