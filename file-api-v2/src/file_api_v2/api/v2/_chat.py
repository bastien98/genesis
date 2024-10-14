from fastapi import APIRouter, Query, Form, Depends

from file_api_v2.dependencies import get_retriever_service, get_users_repo
from file_api_v2.repositories.user_repository import UsersRepository
from file_api_v2.services.retriever_service import RetrieverService

router = APIRouter()


@router.post("/chat")
async def chat(
        username: str = Query(..., description="Active User ID"),
        kb_name: str = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string"),
        retriever: RetrieverService = Depends(get_retriever_service),
        users: UsersRepository = Depends(get_users_repo)
):
    user = users.retrieve_user(username)
    docs = await retriever.fusion_retrieval(query, username, kb_name, user)
    return {"message": "Received", "kb_id": kb_name, "query": query}
