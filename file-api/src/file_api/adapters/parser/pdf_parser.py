from io import BytesIO
from file_api.core.ports.content_parser_port import ContentParserPort
from langchain_core.documents import Document
import PyPDF2


class PdfParser(ContentParserPort):
    async def parse_to_raw_document(self, content: bytes) -> Document:
        reader = PyPDF2.PdfReader(BytesIO(content))
        full_text = ""
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            full_text += text

        document = Document(page_content=full_text)
        return document
