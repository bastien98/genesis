import re
from typing import List

from rank_bm25 import BM25Okapi

from file_api_v2.domain.entities.document import Document
from file_api_v2.domain.entities.user import User
from file_api_v2.ports.storage_port import StoragePort


class Bm25Manager:
    def __init__(self, storage_adapter: StoragePort):
        self.storage_adapter = storage_adapter

    def update_bm25_index(self, user: User, kb_name: str) -> BM25Okapi:
        docs = user.get_knowledge_base(kb_name).docs
        all_text_chunks = []
        for doc in docs:
            all_text_chunks.extend(self.storage_adapter.read_text_chunks(doc.text_chunks_doc_path))

        bm25_index= self.bm25_simple(all_text_chunks)
        print("")
        return bm25_index

    def bm25_simple(self, text_chunks: List[str]):
        """
        Creates a BM25 index from a list of Document objects.

        This function tokenizes each document by splitting the content into words
        (based on whitespace) and then uses the BM25Okapi model from the rank_bm25
        library to create and return a BM25 index.

        Note:
        - This is a basic implementation that splits content by spaces.
        - It can be enhanced by using more advanced text preprocessing techniques
          such as stemming, lemmatization, stopword removal, or custom tokenization.

        Args:
            documents (List[Document]): A list of Document objects, each containing
            the text content to be indexed.

        Returns:
            BM25Okapi: A BM25 index for querying the tokenized documents.
        """

        def preprocess(document):
            document = [re.sub(r'[^\w\s]', '', term.lower().replace('\x00', '')) for term in document]
            return document

        tokenized_documents = [text_chunk.lower().split() for text_chunk in text_chunks]

        docs = []
        for doc in tokenized_documents:
            doc = preprocess(doc)
            docs.append(doc)
        return BM25Okapi(docs)
