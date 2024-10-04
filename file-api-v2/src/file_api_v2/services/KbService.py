from file_api_v2.domain.entities.document import PdfDocument
from file_api_v2.repositories.users_repository import UsersRepository


class KbService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    def add_doc_to_kb(self, username: str, kb_name: str, document: PdfDocument):
        user = self.users_repo.retrieve_user(username)
        user.get_knowledge_base(kb_name).add_document(document)
        self.users_repo.persist_user(user)
        print("")
