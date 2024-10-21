from typing import List

from rank_bm25 import BM25Okapi

from file_api_v2.domain.entities import Document, User, KnowledgeBase, Chunk, BM25Index, RawDocument
from file_api_v2.ports.chunkers import ChunkerPort
from file_api_v2.ports.parsers import ParserPort
from file_api_v2.ports.repositories import ChunkRepository, BM25IndexRepository
from file_api_v2.repositories.raw_document_repository import RawDocumentRepository
from file_api_v2.repositories.user_repository import UserRepository
from file_api_v2.services.context_service import ContextService
from file_api_v2.services.file_storage_service import FileStorageService
from file_api_v2.services.location_service import LocalLocationService
from file_api_v2.services.vector_db_manager import VectorDbService
from file_api_v2.utils.parser import Parser


class KnowledgeBaseService:
    def __init__(
            self,
            file_storage_service: FileStorageService,
            vector_db_service: VectorDbService,
            user_repo: UserRepository,
            parser: Parser,
            context_service: ContextService,
            local_location_service: LocalLocationService

    ):
        self.file_storage_service = file_storage_service
        self.vector_db_service = vector_db_service
        self.user_repo = user_repo
        self.parser = parser
        self.context_service = context_service
        self.local_location_service = local_location_service

    async def add_document(self, raw_doc: RawDocument, username: str, kb_name: str) -> None:
        doc_name = raw_doc.name
        # Get active user
        user = self.user_repo.retrieve_user(username)
        # Calculate locations
        raw_doc_path = self.local_location_service.get_raw_doc_path(username, kb_name, doc_name)
        text_chunks_doc_path = self.local_location_service.get_text_chunks_doc_path(username, kb_name, doc_name)
        md_chunks_doc_path = self.local_location_service.get_md_chunks_doc_path(username, kb_name, doc_name)
        bm25_index_path = self.local_location_service.get_bm25_index_path(username, kb_name)
        # Save the raw document to file storage
        self.file_storage_service.save_raw_file(raw_doc, raw_doc_path)
        # Parse the byte content to text and return pages
        full_text, text_chunks = self.parser.parse_to_text(raw_doc.content)
        # Parse the byte content to Markdown text and return pages
        full_md_text, md_chunks = self.parser.parse_to_markdown(raw_doc.content)
        # Add context to chunks
        ctx_text_chunks = await self.context_service.create_context_chunks(full_text, text_chunks)
        ctx_md_chunks = await self.context_service.create_context_chunks(full_md_text, md_chunks)
        # Save the contextualized chunks to file storage
        self.file_storage_service.save_text_chunks(ctx_text_chunks, text_chunks_doc_path)
        self.file_storage_service.save_md_chunks(ctx_md_chunks, md_chunks_doc_path)
        # Save the chunks in the vector db
        await self.vector_db_service.save_chunks_to_kb(ctx_text_chunks, username, kb_name, doc_name)
        # Update user state to reflect the change
        document = Document(RawDocument.name, RawDocument.source, raw_doc_path, text_chunks_doc_path,
                            md_chunks_doc_path)
        self.user_repo.add_document_to_kb(user, kb_name, document)
        # Update existing BM25 index
        self.bm25_repo.update_bm25_index(user, kb_name)
