from fastapi import APIRouter, Query, Form

router = APIRouter()


@router.post("/chat")
async def chat(
        kb_id: str = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string")
):
    return {"message": "Received", "kb_id": kb_id, "query": query}
