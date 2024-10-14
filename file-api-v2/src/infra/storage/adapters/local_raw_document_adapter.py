import os

from file_api_v2.domain.entities import RawDocument
from file_api_v2.ports.raw_document_port import RawDocumentPort


class LocalRawDocumentAdapter(RawDocumentPort):
    def save_raw_document(self, raw_doc: RawDocument, doc_path: str) -> None:
        directory = os.path.dirname(doc_path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"[INFO] Directory created: {directory}")
        else:
            print(f"[INFO] Directory already exists: {directory}")

        with open(doc_path, 'wb') as f:
            f.write(raw_doc.content)
            print(f"Document saved at {doc_path}")
