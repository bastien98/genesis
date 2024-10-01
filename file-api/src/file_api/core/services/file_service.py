from typing import Tuple, List

from file_api.core.ports.chunker_port import ChunkerPort
from file_api.core.ports.file_parser_port import MarkdownParserPort, TextParserPort
from file_api.core.ports.file_storage_port import FileStoragePort
from langchain_core.documents import Document


class FileStorageService:
    def __init__(self, file_storage: FileStoragePort, markdown_parser: MarkdownParserPort, text_parser: TextParserPort,
                 chunker: ChunkerPort):
        self.file_storage = file_storage
        self.file_parser = markdown_parser
        self.text_parser = text_parser
        self.chunker = chunker

    async def process(self, content: bytes, filename: str, kb_id: str) -> tuple[list[Document], list[Document]]:
        # save raw file
        self.file_storage.save_raw_document(content, filename, kb_id)
        # parse and save markdown file
        md_doc = await self.file_parser.parse_to_markdown_document(content, filename)
        self.file_storage.save_markdown_document(md_doc, filename, kb_id)
        # parse and save text file
        text_doc = await self.text_parser.parse_to_text_document(content)
        self.file_storage.save_text_document(text_doc, filename, kb_id)

        #create markdown and text chunks
        md_chunks = await self.chunker.chunk_document(md_doc)
        text_chunks = await self.chunker.chunk_document(text_doc)

        return md_chunks, text_chunks
