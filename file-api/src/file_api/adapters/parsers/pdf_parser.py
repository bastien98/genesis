from file_api.core.ports.file_parser_port import TextParserPort
from io import BytesIO
import PyPDF2


class PdfParser(TextParserPort):
    async def parse_to_text_chunks(self, content: bytes) -> list[str]:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages_text = []

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text:
                pages_text.append(text)

        return pages_text
