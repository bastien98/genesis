from langchain_core.documents import Document
from llama_parse import LlamaParse

from file_api.config import UNIQUE_PAGE_DELIMMETER
from file_api.core.ports.file_parser_port import MarkdownParserPort


class LlamaParser(MarkdownParserPort):

    async def parse_to_markdown_document(self, content: bytes, filename: str) -> Document:
        parser = LlamaParse(
            result_type="markdown"
        )

        llama_documents = await parser.aload_data(content, extra_info={"file_name": filename})
        combined_text = ""
        for doc in llama_documents:
            combined_text += doc.text + UNIQUE_PAGE_DELIMMETER
        langchain_doc = Document(page_content=combined_text.strip())
        return langchain_doc
