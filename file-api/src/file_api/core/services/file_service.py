from file_api.core.ports.chunker_port import ChunkerPort
from file_api.core.ports.content_parser_port import ContentParserPort
from file_api.core.ports.file_parser_port import FileParserPort
from file_api.core.ports.file_storage_port import FileStoragePort
from langchain_core.documents import Document


class FileStorageService:
    def __init__(self, file_storage: FileStoragePort, content_parser: ContentParserPort, file_parser: FileParserPort,
                 chunker: ChunkerPort):
        self.file_storage = file_storage
        self.content_parser = content_parser
        self.file_parser = file_parser
        self.chunker = chunker

    async def process(self, content: bytes, filename: str) -> list[Document]:
        await self.file_storage.save_raw_content(content, filename)
        clean_document = await self.file_parser.parse_to_clean_document(content, filename)
        await self.file_storage.save_clean_document(clean_document, filename)
        chunks = await self.chunker.chunk_document(clean_document)
        all_documents = await self.file_storage.read_documents(
            self.file_storage.calculate_clean_output_location(filename).get_dir_location)
        # TODO create index for all_documents
        return chunks
