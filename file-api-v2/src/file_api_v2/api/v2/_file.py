from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api_v2.dependencies import get_document_manager, get_kb_service, get_vector_db_manager, get_bm25_manager
from file_api_v2.domain.entities.document import Document
from file_api_v2.services.bm25_manager import Bm25Manager
from file_api_v2.services import cch_service
from file_api_v2.services.document_manager import AbstractDocumentManager
from file_api_v2.services.kb_service import KbService
from file_api_v2.services.vector_db_manager import VectorDbManager
from infra.parsers.adapters.llmama_parse import LlamaParser
from infra.parsers.adapters.pdf_parser import PdfParser

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        document: UploadFile = File(...),
        username: str = Query(..., description="Active User ID"),
        kb_name: str = Query(..., description="Knowledge Base ID"),
        document_manager: AbstractDocumentManager = Depends(get_document_manager),
        vector_db_manager: VectorDbManager = Depends(get_vector_db_manager),
        kb_service: KbService = Depends(get_kb_service),
        bm25_manager: Bm25Manager = Depends(get_bm25_manager)
):
    try:
        content = await document.read()
        doc_name = document.filename

        raw_doc_path = document_manager.saveRAW(content, doc_name, username, kb_name)

        full_text_md, chunked_md = await LlamaParser().parse_to_markdown_chunks(content, doc_name)
        enhanced_md_chunks = await cch_service.create_context_chunks(full_text_md, chunked_md)
        clean_doc_path = document_manager.save_md_chunks(enhanced_md_chunks, doc_name, username, kb_name)
        await vector_db_manager.save_chunks_to_kb(enhanced_md_chunks, username, kb_name, doc_name)

        full_text_txt = await PdfParser().parse_to_text_chunks(content, True)
        chunked_txt = await PdfParser().parse_to_text_chunks(content, False)
        enhanced_chunked_txt = await cch_service.create_context_chunks(full_text_txt, chunked_txt)
        text_chunks_doc_path = document_manager.save_text_chunks(enhanced_chunked_txt, doc_name, username, kb_name)

        document = Document(
            doc_name=doc_name,
            source="NA",
            raw_doc_path=raw_doc_path,
            text_chunks_doc_path=text_chunks_doc_path
        )
        user = kb_service.add_doc_to_kb(username, kb_name, document)

        bm25_index = bm25_manager.update_bm25_index(user, kb_name)
        document_manager.save_bm25_index(bm25_index, username, kb_name)

        return {"message": "Document uploaded and processed successfully.", "document": doc_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
