from typing import List
from langchain_core.documents import Document
from file_api.core.ports.chunker_port import ChunkerPort
from langchain_text_splitters import MarkdownHeaderTextSplitter


class HeaderChunker(ChunkerPort):
    async def chunk_document(self, document: Document) -> List[Document]:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
        chunks = markdown_splitter.split_text(document.page_content)
        return chunks
