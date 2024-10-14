from file_api_v2.domain.entities import RawDocument
from file_api_v2.ports.raw_document_port import RawDocumentPort


class RawDocumentRepository:
    def __init__(self, storage_adapter: RawDocumentPort):
        self.store = storage_adapter

    def save_raw_document(self, raw_doc: RawDocument, doc_path: str) -> None:
        self.store.save_raw_document(raw_doc, doc_path)

