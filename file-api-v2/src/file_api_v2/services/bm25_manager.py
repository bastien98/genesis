import re
from typing import List

from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords

from file_api_v2.domain.entities.document import Document
from file_api_v2.domain.entities.user import User
from file_api_v2.ports.storage_port import StoragePort
from file_api_v2.services.document_manager import DocumentManager

nltk.download('stopwords')


class Bm25Manager:
    def __init__(self, storage_adapter: StoragePort):
        self.storage_adapter = storage_adapter

    def update_bm25_index(self, user: User, kb_name: str) -> BM25Okapi:
        docs = user.get_knowledge_base(kb_name).docs
        all_text_chunks = []
        for doc in docs:
            all_text_chunks.extend(self.storage_adapter.read_text_chunks(doc.text_chunks_doc_path))

        bm25_index = self.bm25_simple(all_text_chunks)
        print("")
        return bm25_index

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
