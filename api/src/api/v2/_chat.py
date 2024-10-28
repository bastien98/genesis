from fastapi import APIRouter, Query, Form, Depends
from langchain_openai import ChatOpenAI

from dependencies import get_knowledge_base_service, get_retriever_service, LLM
from services.knowledge_base_service import KnowledgeBaseService
from services.retriever_service import RetrieverService
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
    fusion = FusionRetriever(retriever_service=retriever_service, user_id=user_id, kb_id=kb_id)
    rag_chain = RagChain(LLM).create_rag_chain(fusion)
    results = rag_chain.invoke({"input": query})
    return {"answer": results["answer"]}
