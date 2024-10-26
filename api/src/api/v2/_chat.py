from fastapi import APIRouter, Query, Form, Depends
from dependencies import get_knowledge_base_service
from services.knowledge_base_service import KnowledgeBaseService

router = APIRouter()


@router.post("/chat")
async def chat(
        user_id: int = Query(..., description="Active User ID"),
        kb_id: int = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string"),
        knowledge_base_service: KnowledgeBaseService = Depends(get_knowledge_base_service)

):
    docs = await knowledge_base_service.retrieve_relevant_chunks_from_kb(query, user_id, kb_id)
    # ranked_docs = reraonker.rank_docs(docs)
    return {"message": "Received", "kb_id": kb_id, "query": query}
