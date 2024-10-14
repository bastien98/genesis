from abc import ABC, abstractmethod
from typing import List

from file_api_v2.domain.entities import Chunk, Document


class ChunkerPort(ABC):
    @abstractmethod
    def chunk_content(self, document: Document) -> List[Chunk]:
        pass
