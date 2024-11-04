from fastapi import APIRouter, Query, Form, Depends

from dependencies import get_knowledge_base_repository
from repositories.knowledge_base_repository import KnowledgeBaseRepository

router = APIRouter()


@router.get("/knowledgebase/list")
async def list_kb(
        user_id: int = Query(..., description="Active User ID"),
        kb_repo: KnowledgeBaseRepository = Depends(get_knowledge_base_repository)
):
    kbs_list = kb_repo.get_all_kb_for_user(user_id= user_id)
    kbs_names_list = [kb.name for kb in kbs_list]

    return kbs_names_list
