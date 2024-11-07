from abc import ABC, abstractmethod
from api.src.domain.entities.raw_document import RawDocument


class ParseToTextPort(ABC):

    @abstractmethod
    def parse_to_text(self,content: bytes) -> tuple[str, list[str]]:
        pass
