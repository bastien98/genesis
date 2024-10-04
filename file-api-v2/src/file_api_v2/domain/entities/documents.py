from dataclasses import dataclass


@dataclass
class PdfDocument:
    doc_name: str
    source: str
    doc_path: str
