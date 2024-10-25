from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from dependencies import get_knowledge_base_service
from domain.entities.raw_document import RawDocument
from services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/knowledge_bases/{kb_id}/documents/add")
async def upload(
        kb_id: int,
        document: UploadFile = File(...),
        user_id: int = Query(..., description="Active User ID"),
        knowledge_base_service: KnowledgeBaseService = Depends(get_knowledge_base_service)

):
    try:
        content = await document.read()
        doc_name = document.filename
        raw_doc = RawDocument(doc_name, "NA", content)
        raw_doc.validate()
        await knowledge_base_service.add_document(raw_doc, user_id, kb_id)
        return {"message": "Document uploaded and processed successfully.", "document": doc_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
