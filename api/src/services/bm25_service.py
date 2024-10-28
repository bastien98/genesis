import re
from typing import List
from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import multiprocessing
import os
import pickle
import logging
from domain.entities.knowledge_base import KnowledgeBase
from services.file_storage_service import FileStorageService
from services.location_service import LocationService

# Ensure necessary NLTK data packages are downloaded
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

class Bm25Service:
    def __init__(self, location_service: LocationService, file_storage_service: FileStorageService):
        self.location_service = location_service
        self.file_storage_service = file_storage_service
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = RegexpTokenizer(r'\w+(?:[-_]\w+)*')
        self.logger = logging.getLogger(__name__)
        # Configure logging level as needed
        logging.basicConfig(level=logging.INFO)

    def update_bm25_index(self, user_id: int, kb: KnowledgeBase) -> None:
        """
        Updates the BM25 index for the given knowledge base by processing all associated documents.
        """
        docs_list = kb.documents
        sorted_docs_list = sorted(docs_list, key=lambda doc: doc.name)

        all_text_chunks = []
        for doc in sorted_docs_list:
            text_chunks_path = self.location_service.get_text_chunks_location(user_id, kb.kb_id, doc.name)
            text_chunks = self.file_storage_service.read_text_chunks(text_chunks_path)
            all_text_chunks.extend(text_chunks)

        bm25_index = self.build_bm25_index(all_text_chunks)
        bm25_location = self.location_service.get_bm25_index_location(user_id, kb.kb_id)
        self.save_bm25_index(bm25_index, bm25_location)

    def build_bm25_index(self, text_chunks: List[str]) -> BM25Okapi:
        """
        Builds a BM25 index from the provided text chunks.
        """
        self.logger.info("Starting BM25 index construction...")

        # Preprocess text chunks using multiprocessing for efficiency
        with multiprocessing.Pool(processes=os.cpu_count()) as pool:
            tokenized_documents = pool.map(self.preprocess_text, text_chunks)

        self.logger.info("Tokenization complete. Building BM25 index...")
        bm25 = BM25Okapi(tokenized_documents)
        self.logger.info("BM25 index construction completed.")

        return bm25

    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocesses a single text chunk: cleans, tokenizes, removes stop words, and lemmatizes.
        """
        # Remove non-printable characters and control characters
        text = re.sub(r'[\x00-\x1F]+', ' ', text)
        text = text.lower()

        # Tokenize text using RegexpTokenizer to retain words with hyphens and underscores
        tokens = self.tokenizer.tokenize(text)

        # Remove stop words
        tokens = [token for token in tokens if token not in self.stop_words]

        # Lemmatize tokens
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]

        return tokens

    def save_bm25_index(self, bm25_index: BM25Okapi, bm25_location: str) -> None:
        """
        Saves the BM25 index to the specified location using pickle serialization.
        """
        self.logger.info(f"Saving BM25 index to {bm25_location}...")
        with open(bm25_location, 'wb') as f:
            pickle.dump(bm25_index, f)
        self.logger.info("BM25 index saved successfully.")

    def load_bm25_index(self, bm25_location: str) -> BM25Okapi:
        """
        Loads the BM25 index from the specified location.
        """
        self.logger.info(f"Loading BM25 index from {bm25_location}...")
        with open(bm25_location, 'rb') as f:
            bm25_index = pickle.load(f)
        self.logger.info("BM25 index loaded successfully.")
        return bm25_index

    def preprocess_query(self, query: str) -> List[str]:
        """
        Preprocesses a user query in the same way documents are preprocessed.
        """
        return self.preprocess_text(query)

    def search(self, bm25_index: BM25Okapi, query: str, top_n: int = 5) -> List[int]:
        """
        Searches the BM25 index with the given query and returns the top N document indices.
        """
        tokenized_query = self.preprocess_query(query)
        self.logger.info(f"Performing BM25 search for query: {query}")
        scores = bm25_index.get_scores(tokenized_query)
        top_n_indices = scores.argsort()[-top_n:][::-1]
        self.logger.info(f"Top {top_n} documents retrieved.")
        return top_n_indices.tolist()