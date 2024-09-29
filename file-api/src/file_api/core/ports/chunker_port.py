from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document


class ChunkerPort(ABC):

    @abstractmethod
    async def chunk_document(self, document: Document) -> List[Document]:
        pass
