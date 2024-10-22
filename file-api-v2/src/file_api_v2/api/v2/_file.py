from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from file_api_v2.dependencies import get_knowledge_base_service
from file_api_v2.domain.entities.raw_document import RawDocument
from file_api_v2.services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()


# Endpoint to upload a file and add its content to an existing knowledge base
@router.post("/upload")
async def upload(
        document: UploadFile = File(...),
        username: str = Query(..., description="Active User ID"),
        kb_name: str = Query(..., description="Knowledge Base ID"),
        knowledge_base_service: KnowledgeBaseService = Depends(get_knowledge_base_service)

):
    try:
        content = await document.read()
        doc_name = document.filename
        raw_doc = RawDocument(doc_name, "NA", content)
        await knowledge_base_service.add_document(raw_doc, username, kb_name)
        return {"message": "Document uploaded and processed successfully.", "document": doc_name}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
