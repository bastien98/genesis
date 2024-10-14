from abc import ABC, abstractmethod

from file_api_v2.domain.entities import RawDocument


class RawDocumentPort(ABC):
    @abstractmethod
    def save_raw_document(self, raw_doc: RawDocument, doc_path: str) -> None:
        pass
