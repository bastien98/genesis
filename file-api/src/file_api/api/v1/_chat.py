from fastapi import APIRouter, Query, Form, Depends

from file_api.core.services.chat_service import ChatService
from file_api.dependencies import get_chat_service

router = APIRouter()


@router.post("/chat")
async def chat(
        kb_id: str = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string"),
        chat_service: ChatService = Depends(get_chat_service)

):
    await chat_service.process(query, kb_id)
    return {"message": "Received", "kb_id": kb_id, "query": query}
