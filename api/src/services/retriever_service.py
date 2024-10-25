from typing import List
import numpy as np
from repositories.knowledge_base_repository import KnowledgeBaseRepository
from services.file_storage_service import FileStorageService
from services.location_service import LocationService
from services.vector_db_service import VectorDbService


class RetrieverService:
    def __init__(self, location_service: LocationService, kb_repo: KnowledgeBaseRepository,
                 vectordb_service: VectorDbService, file_storage_service: FileStorageService):
        self.location_service = location_service
        self.kb_repo = kb_repo
        self.vectordb_service = vectordb_service
        self.file_storage_service = file_storage_service

    async def fusion_retrieval(self, query: str, user_id: int, kb_id: int, alpha: float = 0.5,  # Bigger alpha means more wheigth to vector similarity search
                               k: int = 20) -> List[str]:
        kb = self.kb_repo.get_by_id(kb_id)
        docs_list = kb.documents
        sorted_docs_list = sorted(docs_list, key=lambda doc: doc.name)
        docs_index = {doc.name: index for index, doc in enumerate(sorted_docs_list)} # Creates a dictionary from docs_list with key: doc_name and value: index in docs_list

        kb_doc_count = await self.vectordb_service.get_kb_document_count(kb_id)

        all_docs_with_score = await self.vectordb_service.similarity_search_with_score(query, kb_id, kb_doc_count)
        bm25_index = self.file_storage_service.read_BM25_index(
            self.location_service.get_bm25_index_location(user_id, kb_id))
        bm25_scores = bm25_index.get_scores(query.lower().split())

        sorted_documents = sorted(
            all_docs_with_score,
            key=lambda doc_tuple: (
                docs_index.get(doc_tuple[0].metadata.get('filename'), float('inf')),
                doc_tuple[0].metadata.get('chunk_number', float('inf')),
                doc_tuple[1]  # Adding the 'number' from the tuple for sorting
            )
        )

        vector_scores = np.array([score for _, score in sorted_documents])
        vector_scores = 1 - (vector_scores - np.min(vector_scores)) / (np.max(vector_scores) - np.min(vector_scores))

        bm25_scores = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores))

        # Combine scores
        combined_scores = alpha * vector_scores + (1 - alpha) * bm25_scores

        # Rank documents
        sorted_indices = np.argsort(combined_scores)[::-1]

        # Return top k documents
        return [sorted_documents[i][0].page_content for i in sorted_indices[:k]]
