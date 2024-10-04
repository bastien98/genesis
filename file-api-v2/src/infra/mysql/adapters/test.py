from sqlalchemy import create_engine

from file_api_v2.domain.entities.document import PdfDocument
from file_api_v2.services.document_manager import LocalFileSystemDocumentManager
from infra.mysql.adapters.knowledge_base_adapter import KnowledgeBaseAdapter

engine = create_engine("mysql+mysqlconnector://root:Gilles1998@localhost/superRag")
adapter = KnowledgeBaseAdapter(engine)

try:
    kb = adapter.retrieve_knowledge_base_for_user(user_id=1, kb_id=1)
    print(f"Knowledge Base: {kb.kb_id}, BM25 Index Location: {kb.bm25_index_location}")
    adapter.add_pdf_document_for_user_and_kb(1, 1, PdfDocument(
        username="bastien", kb_name="kb-1", doc_name="test", source="NA", document_manager=LocalFileSystemDocumentManager(), content=bytes()
    ))
except Exception as e:
    print(e)
