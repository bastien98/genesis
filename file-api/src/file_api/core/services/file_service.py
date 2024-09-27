from file_api.core.ports.content_parser_port import ContentParserPort
from file_api.core.ports.file_parser_port import FileParserPort
from file_api.core.ports.file_storage_port import FileStoragePort, FileLocation


class FileStorageService:
    def __init__(self, file_storage: FileStoragePort, content_parser: ContentParserPort, file_parser: FileParserPort):
        self.file_storage = file_storage
        self.content_parser = content_parser
        self.file_parser = file_parser

    async def process(self, content: bytes, filename: str) -> FileLocation:
        raw_location = await self.file_storage.save_raw_content(content, filename)
        await self.content_parser.parse_to_raw_document(content)
        clean_document = await self.file_parser.parse_to_clean_document(raw_location)
        return await self.file_storage.save_clean_document(clean_document, raw_location)