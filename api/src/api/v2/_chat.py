from fastapi import APIRouter, Query, Form, Depends
from langchain_openai import ChatOpenAI

from dependencies import get_knowledge_base_service, get_retriever_service, LLM
from services.knowledge_base_service import KnowledgeBaseService
from services.retriever_service import RetrieverService
from utils.Agent import KbAgent
from utils.fusion_retriever import FusionRetriever
from utils.rag_chain import RagChain

router = APIRouter()


@router.post("/chat")
async def chat(
        user_id: int = Query(..., description="Active User ID"),
        kb_id: int = Query(..., description="Knowledge Base ID"),
        query: str = Form(..., description="Query string"),
        retriever_service: RetrieverService = Depends(get_retriever_service)

):
    fusion_retriever = FusionRetriever(retriever_service=retriever_service, user_id=user_id, kb_id=kb_id)
    agent = KbAgent(LLM, fusion_retriever)
    response = agent.execute_agent(None, query)
    print("")
    return {"answer": response.get("messages")[-1].content}
