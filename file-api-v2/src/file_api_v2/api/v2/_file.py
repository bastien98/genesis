from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api_v2.dependencies import get_document_manager, get_kb_service
from file_api_v2.domain.entities.document import PdfDocument
from file_api_v2.services import KbService
from file_api_v2.services.document_manager import AbstractDocumentManager

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        document: UploadFile = File(...),
        username: str = Query(..., description="Active User ID"),
        kb_name: str = Query(..., description="Knowledge Base ID"),
        document_manager: AbstractDocumentManager = Depends(get_document_manager),
        kb_service: KbService = Depends(get_kb_service)
):
    try:
        content = await document.read()
        doc_name = document.filename
        doc_path = document_manager.savePDF(content, doc_name, username, kb_name)
        document = PdfDocument(
            doc_name=doc_name,
            source="NA",
            doc_path=doc_path
        )
        kb_service.add_doc_to_kb(username, kb_name, document)

        return {"message": "Document uploaded and processed successfully.", "document": doc_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
