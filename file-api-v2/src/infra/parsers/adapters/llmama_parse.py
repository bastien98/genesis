from llama_parse import LlamaParse

from file_api_v2.config import UNIQUE_PAGE_DELIMMETER
from file_api_v2.ports.parser_port import MarkdownParserPort


class LlamaParser(MarkdownParserPort):

    async def parse_to_markdown_document(self, content: bytes, filename: str) -> list[str]:
        parser = LlamaParse(
            result_type="markdown"
        )
        llama_documents = await parser.aload_data(content, extra_info={"file_name": filename})
        text_chunks = [chunk + UNIQUE_PAGE_DELIMMETER for chunk in llama_documents]
        return text_chunks
