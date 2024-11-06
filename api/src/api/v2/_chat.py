from fastapi import APIRouter, Query, Form, Depends
from dependencies import get_retriever_service, LLM
from services.retriever_service import RetrieverService
from utils.agent import KbAgent
from utils.fusion_retriever import FusionRetriever

router = APIRouter()


@router.post("/chat")
async def chat(
        user_id: int = Query(..., description="Active User ID"),
        kb_id: int = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string"),
        retriever_service: RetrieverService = Depends(get_retriever_service)

):
    fusion_retriever_for_kb = FusionRetriever(retriever_service=retriever_service, user_id=user_id, kb_id=kb_id)
    agent = KbAgent(LLM, fusion_retriever_for_kb)
    response = agent.execute_agent(None, query)
    print("")
    return {"answer": response.get("messages")[-1].content}
