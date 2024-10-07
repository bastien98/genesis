from dataclasses import dataclass


@dataclass
class Document:
    doc_name: str
    source: str
    raw_doc_path: str
    text_chunks_doc_path: str
