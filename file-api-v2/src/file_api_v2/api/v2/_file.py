from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api_v2.dependencies import get_document_manager, get_kb_service, get_vector_db_manager
from file_api_v2.domain.entities.document import Document
from file_api_v2.services import KbService
from file_api_v2.services.document_manager import AbstractDocumentManager
from file_api_v2.services.vector_db_manager import VectorDbManager
from infra.parsers.adapters.llmama_parse import LlamaParser

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        document: UploadFile = File(...),
        username: str = Query(..., description="Active User ID"),
        kb_name: str = Query(..., description="Knowledge Base ID"),
        document_manager: AbstractDocumentManager = Depends(get_document_manager),
        vector_db_manager: VectorDbManager = Depends(get_vector_db_manager),
        kb_service: KbService = Depends(get_kb_service)
):
    try:
        content = await document.read()
        doc_name = document.filename
        raw_doc_path = document_manager.saveRAW(content, doc_name, username, kb_name)
        md_chunks = await LlamaParser().parse_to_markdown_chunks(content, doc_name)
        clean_doc_path = document_manager.saveCLEAN(md_chunks, doc_name, username, kb_name)
        await vector_db_manager.save_chunks_to_kb(md_chunks, username, kb_name)
        document = Document(
            doc_name=doc_name,
            source="NA",
            raw_doc_path=raw_doc_path,
            clean_doc_path=clean_doc_path
        )
        user = kb_service.add_doc_to_kb(username, kb_name, document)


        return {"message": "Document uploaded and processed successfully.", "document": doc_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
