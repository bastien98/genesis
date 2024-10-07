from typing import List
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi


def bm25_simple(documents: List[Document]) -> BM25Okapi:
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
    tokenized_documents = [doc.page_content.split() for doc in documents]
    # TODO: clean tokenized_document (worden zitten nu vol markdown syntax and ():;...)
    return BM25Okapi(tokenized_documents)
