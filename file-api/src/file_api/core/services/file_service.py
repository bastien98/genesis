from file_api.core.ports.chunker_port import ChunkerPort
from file_api.core.ports.file_parser_port import FileParserPort
from file_api.core.ports.file_storage_port import FileStoragePort
from langchain_core.documents import Document


class FileStorageService:
    def __init__(self, file_storage: FileStoragePort, file_parser: FileParserPort,
                 chunker: ChunkerPort):
        self.file_storage = file_storage
        self.file_parser = file_parser
        self.chunker = chunker

    async def process(self, content: bytes, filename: str, kb_id: str) -> list[Document]:
        await self.file_storage.save_raw_content(content, filename, kb_id)
        clean_document = await self.file_parser.parse_to_clean_document(content, filename)
        await self.file_storage.save_clean_document(clean_document, filename)
        chunks = await self.chunker.chunk_document(clean_document)
        return chunks
