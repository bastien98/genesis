from typing import Callable, List
from rank_bm25 import BM25Okapi

BM25IndexingStrategy = Callable[[List[str]], BM25Okapi]
