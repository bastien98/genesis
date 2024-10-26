from typing import List

from domain.entities.document import Document
from domain.entities.raw_document import RawDocument
from repositories.document_repository import DocumentRepository
from repositories.knowledge_base_repository import KnowledgeBaseRepository
from repositories.user_repository import UserRepository
from services.bm25_service import Bm25Service
from services.context_service import ContextService
from services.file_storage_service import FileStorageService
from services.location_service import LocationService
from services.retriever_service import RetrieverService
from services.vector_db_service import VectorDbService
from utils.parser import Parser


class KnowledgeBaseService:
    def __init__(
            self,
            file_storage_service: FileStorageService,
            vector_db_service: VectorDbService,
            parser: Parser,
            context_service: ContextService,
            location_service: LocationService,
            bm25_service: Bm25Service,
            user_repo: UserRepository,
            kb_repo: KnowledgeBaseRepository,
            document_repo: DocumentRepository,
            retriever_service: RetrieverService
    ):
        self.file_storage_service = file_storage_service
        self.vector_db_service = vector_db_service
        self.parser = parser
        self.context_service = context_service
        self.location_service = location_service
        self.bm25_service = bm25_service
        self.user_repo = user_repo
        self.kb_repo = kb_repo
        self.document_repo = document_repo
        self.retriever_service = retriever_service

    async def add_document(self, raw_doc: RawDocument, user_id: int, kb_id: int) -> None:
        # Add document to knowledge base in domain (business rules are applied here)
        document = Document(name=raw_doc.name, source=raw_doc.source)
        kb = self.kb_repo.get_by_id(kb_id)
        kb.add_document(document)

        # Add document in external systems
        # Calculate file storage locations
        doc_name = raw_doc.name
        raw_doc_path = self.location_service.get_raw_doc_location(user_id, kb_id, doc_name)
        text_chunks_doc_path = self.location_service.get_text_chunks_location(user_id, kb_id, doc_name)
        md_chunks_doc_path = self.location_service.get_md_chunks_doc_location(user_id, kb_id, doc_name)

        # Save the raw document to file storage
        self.file_storage_service.save_raw_document(raw_doc, raw_doc_path)

        # Parse the byte content to text and return full text and page list
        full_text, text_chunks = self.parser.parse_to_text(raw_doc.content)

        # Parse the byte content to Markdown text and return full text and page list
        full_md_text, md_chunks = await self.parser.parse_to_markdown(raw_doc)

        # Add context to chunks
        print("Adding context to text chunks")
        ctx_text_chunks = await self.context_service.create_context_chunks(full_text, text_chunks)
        print("Done adding context to text chunks")
        print("Adding context to md chunks")
        ctx_md_chunks = await self.context_service.create_context_chunks(full_md_text, md_chunks)
        print("Done adding context to mo chunks")

        # Save the contextualized chunks to file storage
        self.file_storage_service.save_text_chunks(ctx_text_chunks, text_chunks_doc_path)
        self.file_storage_service.save_md_chunks(ctx_md_chunks, md_chunks_doc_path)

        # Save the md chunks in the vector db
        await self.vector_db_service.save_chunks_to_kb(ctx_md_chunks, kb_id, doc_name)

        # Persist changed state
        self.document_repo.add(kb_id, document)

        # Update existing BM25 index
        self.bm25_service.update_bm25_index(user_id, kb)

    async def retrieve_relevant_chunks_from_kb(self, query: str, user_id: int, kb_id: int) -> List[str]:
        return await self.retriever_service.fusion_retrieval(query, user_id, kb_id)

