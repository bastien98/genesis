from typing import List

import numpy as np

from file_api_v2.domain.entities.entities import User
from file_api_v2.ports.vector_db_port import VectorDbPort
from file_api_v2.services.document_manager import AbstractDocumentManager


class RetrieverService:
    def __init__(self, vector_db: VectorDbPort, document_manager: AbstractDocumentManager):
        self.vector_db = vector_db
        self.document_manager = document_manager

    async def fusion_retrieval(self, query: str, username: str, kb_name: str, user: User, alpha: float = 0.5,
                               docs_to_retrieve: int = 20) -> List[str]:
        kb_name_in_vdb = f"{username}_{kb_name}"
        docs_list = user.get_knowledge_base(kb_name).docs
        sorted_docs_list = sorted(docs_list, key=lambda doc: doc.doc_name)
        filename_index = {doc.doc_name: index for index, doc in enumerate(sorted_docs_list)}

        count = self.vector_db.get_kb_document_count(kb_name_in_vdb)


        all_docs_with_score = await self.vector_db.similarity_search_with_score(query, kb_name_in_vdb, count)
        bm25_index = self.document_manager.read_bm25_index(username, kb_name)
        bm25_scores = bm25_index.get_scores(query.lower().split())

        sorted_documents = sorted(
            all_docs_with_score,
            key=lambda doc_tuple: (
                filename_index.get(doc_tuple[0].metadata.get('filename'), float('inf')),
                doc_tuple[0].metadata.get('chunk_number', float('inf')),
                doc_tuple[1]  # Adding the 'number' from the tuple for sorting
            )
        )

        vector_scores = np.array([score for _, score in sorted_documents])
        vector_scores = 1 - (vector_scores - np.min(vector_scores)) / (np.max(vector_scores) - np.min(vector_scores))

        bm25_scores = (bm25_scores - np.min(bm25_scores)) / (np.max(bm25_scores) - np.min(bm25_scores))

        # Step 5: Combine scores
        combined_scores = alpha * vector_scores + (1 - alpha) * bm25_scores

        # Step 6: Rank documents
        sorted_indices = np.argsort(combined_scores)[::-1]

        # Step 7: Return top k documents
        return [sorted_documents[i][0].page_content for i in sorted_indices[:docs_to_retrieve]]
