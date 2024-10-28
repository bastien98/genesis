import asyncio
from typing import Any, List

from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

from services.retriever_service import RetrieverService


class FusionRetriever(BaseRetriever):
    retriever_service: RetrieverService
    user_id: int
    kb_id: int

    def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun) -> list[Document]:
        doc_list = asyncio.run(self.retriever_service.fusion_retrieval(query, self.user_id, self.kb_id))
        return self.map_strings_to_documents(doc_list)

    def map_strings_to_documents(self, docs: List[str]) -> List[Document]:
        return [Document(page_content=text) for text in docs]
