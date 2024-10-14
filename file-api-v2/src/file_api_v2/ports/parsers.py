from abc import ABC, abstractmethod

from file_api_v2.domain.entities import RawDocument, Document


class ParserPort(ABC):
    @abstractmethod
    def parse_to_markdown(self, document: RawDocument) -> Document:
        pass

    @abstractmethod
    def parse_to_text(self, document: RawDocument) -> Document:
        pass
