import re
from typing import List
from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
from domain.entities.knowledge_base import KnowledgeBase
from ports.storage_port import FileStoragePort
from services.location_service import LocalLocationService

nltk.download('stopwords')


class Bm25Service:
    def __init__(self, location_service: LocalLocationService, storage_adapter: FileStoragePort):
        self.location_service = location_service
        self.storage_adapter = storage_adapter

    def update_bm25_index(self, username: str, kb: KnowledgeBase) -> None:
        docs_list = kb.documents
        sorted_docs_list = sorted(docs_list, key=lambda doc: doc.name)

        all_text_chunks = []
        for doc in sorted_docs_list:
            text_chunks_path = self.location_service.get_text_chunks_location(username, kb.kb_id, doc.name)
            all_text_chunks.extend(self.storage_adapter.read_text_chunks(text_chunks_path))

        bm25_index = self.bm25_simple(all_text_chunks)
        bm25_location = self.location_service.get_bm25_index_location(username, kb.kb_id)
        self.storage_adapter.save_BM25_index(bm25_index, bm25_location)

    def bm25_simple(self, text_chunks: List[str]) -> BM25Okapi:
        stop_words = set(stopwords.words('english'))

        def preprocess_text(text):
            text = text.replace('\x00', '').lower()
            text = re.sub(r'[^\w\s]', '', text)
            tokens = text.split()
            tokens = [word for word in tokens if word not in stop_words]
            return tokens

        tokenized_documents = [
            preprocess_text(text_chunk)
            for text_chunk in text_chunks
        ]

        return BM25Okapi(tokenized_documents)
