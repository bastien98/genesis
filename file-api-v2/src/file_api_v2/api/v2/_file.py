from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api.core.services.file_service import FileStorageService
from file_api.core.services.kb_service import KBService
from file_api.dependencies import get_file_service, get_kb_service
from file_api_v2.dependencies import get_document_manager
from file_api_v2.domain.entities.documents import PdfDocument
from file_api_v2.utills.document_manager import AbstractDocumentManager

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        file: UploadFile = File(...),
        user_id: str = Query(..., description="Active User ID"),
        kb_id: str = Query(..., description="Knowledge Base ID"),
        kb_service: KbService = Depends(get_kb_service),
        document_manager: AbstractDocumentManager = Depends(get_document_manager)
):
    try:
        document = PdfDocument(
            username=user_id,
            kb_name=kb_id,
            doc_id=str(file.filename),
            source="NA",
            document_manager=document_manager,
            content=await file.read()
        )
        md_chunks = kb_service.add_doc_to_kb(user_id, kb_id, document)
        await kb_service.update(md_chunks, kb_id)
        return {"message": "File uploaded and processed successfully.", "filename": file.filename}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
