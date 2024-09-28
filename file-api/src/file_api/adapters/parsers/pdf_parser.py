from io import BytesIO
from file_api.core.ports.content_parser_port import ContentParserPort
import PyPDF2


class PdfParser(ContentParserPort):
    async def parse_to_text(self, content: bytes) -> str:
        reader = PyPDF2.PdfReader(BytesIO(content))
        full_text = ""
        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            full_text += text

        return full_text.strip()
