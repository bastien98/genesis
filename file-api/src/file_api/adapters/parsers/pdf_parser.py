from io import BytesIO
import PyPDF2
from langchain_core.documents import Document

from file_api.core.ports.file_parser_port import TextParserPort


class PdfParser(TextParserPort):
    async def parse_to_text_document(self, content: bytes) -> Document:
        reader = PyPDF2.PdfReader(BytesIO(content))
        full_text = ""
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            full_text += text

        return Document(page_content=full_text)
