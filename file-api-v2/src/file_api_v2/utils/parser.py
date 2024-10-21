from io import BytesIO
from typing import List, Tuple

import PyPDF2
from llama_parse import LlamaParse


class Parser:
    @staticmethod
    def parse_to_text(content: bytes, as_single_string: bool = False) -> tuple[str, list[str]]:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages_text = []

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text:
                pages_text.append(text)

        return "\n".join(pages_text), pages_text

    @staticmethod
    def parse_to_markdown(content: bytes, as_single_string: bool = False) -> tuple[str, list[str]]:
        parser = LlamaParse(
            result_type="markdown"
        )
        llama_documents = parser.load_data(content)
        pages = [page.text for page in llama_documents]

        return "\n".join(pages), pages
