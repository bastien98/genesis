from dataclasses import dataclass


@dataclass
class Document:
    doc_name: str
    source: str
    raw_doc_path: str
    clean_doc_path: str
