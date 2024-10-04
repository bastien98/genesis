class KnowledgeBase:
    def __init__(self, user_id: int, kb_id: int, doc_ids: list[int], kb_name: str, bm25_index_location: str):
        self.user_id = user_id
        self.kb_id = kb_id
        self.doc_ids = doc_ids
        self.kb_kb_name = kb_name
        self.bm25_index_location = bm25_index_location
