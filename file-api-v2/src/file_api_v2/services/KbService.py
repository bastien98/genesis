from file_api_v2.domain.entities.documents import PdfDocument


class KbService:
    def __init__(self, kb_repository: KbRepository):
        self.kb_repository = kb_repository

    def add_doc_to_kb(self, user_id: str, kb_id: str, document: PdfDocument):
        kb = self.kb_repository.retrieve_kb(user_id, kb_id)
