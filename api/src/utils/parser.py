from io import BytesIO
import PyPDF2
from llama_parse import LlamaParse
from domain.entities.raw_document import RawDocument


class Parser:
    @staticmethod
    def parse_to_text(content: bytes) -> tuple[str, list[str]]:
        reader = PyPDF2.PdfReader(BytesIO(content))
        pages_text = []

        for page_number in range(len(reader.pages)):
            page = reader.pages[page_number]
            text = page.extract_text()
            if text:
                pages_text.append(text)

        return "\n".join(pages_text), pages_text

    @staticmethod
    async def parse_to_markdown(doc: RawDocument) -> tuple[str, list[str]]:
        parser = LlamaParse(
            result_type="markdown"
        )
        llama_documents = await parser.aload_data(doc.content, extra_info={'file_name': doc.name})
        print("Parsing to markdown finished")
        pages = [page.text for page in llama_documents]

        return "\n".join(pages), pages