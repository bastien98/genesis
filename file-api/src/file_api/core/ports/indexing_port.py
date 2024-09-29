from typing import Callable, List
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

BM25IndexingStrategy = Callable[[List[Document]], BM25Okapi]
