from abc import ABC, abstractmethod
from typing import Any


class FileStoragePort(ABC):
    @abstractmethod
    async def save_file(self, file: Any, file_name: str, path: str) -> str:
        """Save a file to a given path. Returns the full path to the file."""
        pass
