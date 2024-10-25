from ports.location_port import LocationPort


class LocationService:
    def __init__(self, location_service: LocationPort):
        self.location_service = location_service

    def get_raw_doc_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        return self.location_service.get_raw_doc_location(user_id, kb_id, doc_name)

    def get_md_chunks_doc_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        return self.location_service.get_md_chunks_doc_location(user_id, kb_id, doc_name)

    def get_text_chunks_location(self, user_id: int, kb_id: int, doc_name: str) -> str:
        return self.location_service.get_text_chunks_location(user_id, kb_id, doc_name)

    def get_bm25_index_location(self, user_id: int, kb_id: int) -> str:
        return self.location_service.get_bm25_index_location(user_id, kb_id)
