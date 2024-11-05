from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from dependencies import get_knowledge_base_service, get_knowledge_base_repository
from domain.entities.raw_document import RawDocument
from repositories.knowledge_base_repository import KnowledgeBaseRepository
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



@router.get("/get_knowledge_bases")
async def get_knowledge_bases(
        user_id: int = Query(..., description="Active User ID"),
        kb_repo: KnowledgeBaseRepository = Depends(get_knowledge_base_repository)
):
    kbs_list = kb_repo.list_kbs_for_user(user_id= user_id)
    kbs_data = [
        {
            'id': kb.kb_id,
            'title': kb.name,
            'icon': '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 256.000000 256.000000" preserveAspectRatio="xMidYMid meet"> <g transform="translate(0.000000,256.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none"> <path d="M1080 2393 c-375 -26 -631 -87 -721 -172 -23 -23 -39 -47 -39 -61 0 -38 69 -95 157 -128 393 -151 1293 -143 1643 14 64 29 120 82 120 114 0 32 -56 85 -120 114 -199 89 -681 145 -1040 119z"/> <path d="M320 1737 c0 -235 0 -236 24 -264 51 -60 239 -125 459 -157 496 -74 1153 -16 1368 120 69 43 69 42 69 303 l0 234 -27 -28 c-110 -109 -491 -185 -933 -185 -442 0 -823 76 -933 185 l-27 28 0 -236z"/> <path d="M320 1097 c0 -235 0 -236 24 -264 51 -60 239 -125 459 -157 496 -74 1153 -16 1368 120 69 43 69 42 69 303 l0 234 -27 -28 c-110 -109 -491 -185 -933 -185 -442 0 -823 76 -933 185 l-27 28 0 -236z"/> <path d="M320 457 c0 -235 0 -236 24 -264 51 -60 239 -125 459 -157 496 -74 1153 -16 1368 120 69 43 69 42 69 303 l0 234 -27 -28 c-110 -109 -491 -185 -933 -185 -442 0 -823 76 -933 185 l-27 28 0 -236z"/> </g> </svg>'

        } for kb in kbs_list
    ]
    return kbs_data