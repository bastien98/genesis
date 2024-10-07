from file_api_v2.domain.entities.document import Document
from file_api_v2.domain.entities.user import User
from file_api_v2.ports.indexing_port import BM25IndexingStrategy
from file_api_v2.ports.storage_port import StoragePort


class Bm25Manager:
    def __init__(self, bm25_index_creator: BM25IndexingStrategy, storage_adapter: StoragePort):
        self.bm25_index_creator = bm25_index_creator
        self.storage_adapter = storage_adapter

    def update_bm25_index(self, user: User, kb_name: str):
        docs = user.get_knowledge_base(kb_name).docs
        docs[0].raw_doc_path

