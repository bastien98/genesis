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

    async def process(self, content: bytes, filename: str, kb_id: str) -> list[Document]:
        await self.file_storage.save_raw_content(content, filename, kb_id)
        md_doc = await self.file_parser.parse_to_markdown_document(content, filename)
        await self.file_storage.save_markdown_document(md_doc, filename, kb_id)
        text_doc = await self.text_parser.parse_to_text_document(content)
        self.file_storage.save_text_document(text_doc, filename, kb_id)
        chunks = await self.chunker.chunk_document(md_doc)
        return chunks
