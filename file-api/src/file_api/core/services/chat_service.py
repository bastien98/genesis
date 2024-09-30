from typing import List

import numpy as np
from langchain_core.documents import Document

from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.vector_db_port import VectorDbPort


class ChatService:
    def __init__(self, vector_db: VectorDbPort, file_storage: FileStoragePort):
        self._vector_db = vector_db
        self._file_storage = file_storage

    async def process(self, query: str, kb_id: str) -> str:
        retrieved_docs = await self.fusion_retrieval(kb_id, query, 20)
        return "ok"

    async def fusion_retrieval(self, kb_id: str, query: str, num_docs_to_retrieve: int, alpha: float = 0.5) -> list[Document]:
        count = self._vector_db.get_kb_document_count(kb_id)
        retrieved_docs = await self._vector_db.similarity_search(query, kb_id, count)
        retrieved_docs_with_score = await self._vector_db.similarity_search_with_score(query, kb_id, count)
        BM25_index = await self._file_storage.get_BM25_index(kb_id)
        BM25_scores = BM25_index.get_scores(query.split())

        vector_scores = np.array([score for _, score in retrieved_docs_with_score])
        vector_scores = 1 - (vector_scores - np.min(vector_scores)) / (np.max(vector_scores) - np.min(vector_scores))

        bm25_scores = (BM25_scores - np.min(BM25_scores)) / (np.max(BM25_scores) - np.min(BM25_scores))

        # Step 5: Combine scores
        combined_scores = alpha * vector_scores + (1 - alpha) * bm25_scores

        # Step 6: Rank documents
        sorted_indices = np.argsort(combined_scores)[::-1]

        # Step 7: Return top k documents
        return [retrieved_docs[i] for i in sorted_indices[:num_docs_to_retrieve]]
