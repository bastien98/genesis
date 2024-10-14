from typing import List

from rank_bm25 import BM25Okapi

from file_api_v2.domain.entities import Document, User, KnowledgeBase, Chunk, BM25Index, RawDocument
from file_api_v2.ports.chunkers import ChunkerPort
from file_api_v2.ports.parsers import ParserPort
from file_api_v2.ports.repositories import RawDocumentRepository, ChunkRepository, BM25IndexRepository


class KnowledgeBaseService:
    def __init__(
            self,
            document_repo: RawDocumentRepository,
            chunk_repo: ChunkRepository,
            bm25_repo: BM25IndexRepository,
            user_repo: UserRepository,
            parser: ParserPort,
            chunker: ChunkerPort,
            context_service: ContextService

    ):
        self.document_repo = document_repo
        self.chunk_repo = chunk_repo
        self.bm25_repo = bm25_repo
        self.user_repo = user_repo
        self.parser = parser
        self.chunker = chunker
        self.context_service = context_service

    def add_document(self, raw_doc: RawDocument, username: str, kb: KnowledgeBase) -> None:
        # Get active user
        user = self.user_repo.find_by_username(username)
        # Calculate locations
        raw_doc_path = self.location_service.get_raw_doc_path(user, kb, raw_doc)
        text_chunks_doc_path = self.location_service.get_text_chunks_doc_path(user, kb, raw_doc)
        md_chunks_doc_path = self.location_service.get_md_chunks_doc_path(user, kb, raw_doc)
        bm25_index_path = self.location_service.get_bm25_index_path(user, kb)
        # Save the document
        self.document_repo.save_raw_document(raw_doc, raw_doc_path, user, kb)
        # Parse the byte content to text
        text_content = self.parser.parse_to_text(raw_doc)
        # Parse the byte content to Markdown text
        md_content = self.parser.parse_to_markdown(raw_doc)
        # Split the documents into chunks
        text_chunks = self.chunker.chunk_content(text_content)
        md_chunks = self.chunker.chunk_content(md_content)
        # Add context to chunks
        ctx_text_chunks = self.context_service.create_context_chunks(text_chunks)
        ctx_md_chunks = self.context_service.create_context_chunks(md_chunks)
        # Save the chunks
        self.chunk_repo.save_chunks(ctx_text_chunks, text_chunks_doc_path, user, kb)
        self.chunk_repo.save_chunks(ctx_md_chunks, md_chunks_doc_path, user, kb)
        # Update user state to reflect the change
        document = Document(RawDocument.name, RawDocument.source, raw_doc_path, text_chunks_doc_path,
                            md_chunks_doc_path)
        self.user_repo.add_document_to_kb(user, kb, document)
        # Update BM25 index
        self.bm25_repo.update_bm25_index(user, kb)
