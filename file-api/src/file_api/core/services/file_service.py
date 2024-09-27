import asyncio

from file_api.core.ports.chunker_port import ChunkerPort
from file_api.core.ports.content_parser_port import ContentParserPort
from file_api.core.ports.file_parser_port import FileParserPort
from file_api.core.ports.file_storage_port import FileStoragePort, FileLocation


class FileStorageService:
    def __init__(self, file_storage: FileStoragePort, content_parser: ContentParserPort, file_parser: FileParserPort,
                 chunker: ChunkerPort):
        self.file_storage = file_storage
        self.content_parser = content_parser
        self.file_parser = file_parser
        self.chunker = chunker

    async def process(self, content: bytes, filename: str) -> FileLocation:
        save_raw_task = asyncio.create_task(
            self.file_storage.save_raw_content(content, filename)
        )
        parse_raw_task = asyncio.create_task(
            self.content_parser.parse_to_raw_document(content)
        )

        # Wait for both tasks to complete
        raw_location, _ = await asyncio.gather(save_raw_task, parse_raw_task)

        # Proceed to step 3
        clean_document = await self.file_parser.parse_to_clean_document(raw_location)

        # Run steps 4 and 5 concurrently
        save_clean_task = asyncio.create_task(
            self.file_storage.save_clean_document(clean_document, raw_location)
        )
        chunk_document_task = asyncio.create_task(
            self.chunker.chunk_document(clean_document)
        )

        # Wait for both tasks to complete
        clean_location, _ = await asyncio.gather(save_clean_task, chunk_document_task)

        return clean_location
