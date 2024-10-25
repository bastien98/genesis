from dataclasses import dataclass


@dataclass
class RawDocument:
    name: str
    source: str
    content: bytes

    def validate(self):
        self.validate_document_is_pdf()

    def validate_document_is_pdf(self) -> None:
        """Validate that the document is a PDF."""
        if not self.name.lower().endswith('.pdf'):
            raise ValueError(f"The document '{self.name}' is not a PDF file.")
