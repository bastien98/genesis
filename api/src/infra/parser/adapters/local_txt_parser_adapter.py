import PyPDF2
from io import BytesIO
from ports.parse_to_text_port import ParseToTextPort


class LocalTxtParserAdapter(ParseToTextPort):

    def parse_to_text(self, content: bytes) -> tuple[str, list[str]]:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages_text = []

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text:
                pages_text.append(text)

        return "\n".join(pages_text), pages_text