from typing import Type

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from file_api_v2.domain.entities.knowledge_base import KnowledgeBase
from file_api_v2.domain.entities.document import Document
from file_api_v2.ports.knowledge_base_port import KnowledgeBasePort
from infra.mysql.dtos import KnowledgeBaseDTO, DocumentDto


class KnowledgeBaseAdapter(KnowledgeBasePort):
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def retrieve_knowledge_base_for_user(self, user_id: int, kb_id: int) -> KnowledgeBase:
        with Session(bind=self.db_engine) as session:
            try:
                knowledge_base_dto = session.query(KnowledgeBaseDTO).filter_by(user_id=user_id, kb_id=kb_id).first()
                if not knowledge_base_dto:
                    raise Exception(f"KnowledgeBase with user_id {user_id} and kb_id {kb_id} not found.")

                return map_knowledge_base_dto_to_domain(knowledge_base_dto)

            except Exception as e:
                print(f"Error retrieving KnowledgeBase: {e}")
                raise

    # def add_pdf_document_for_user_and_kb(self, user_id: int, kb_id: int, pdf_doc: PdfDocument):
    #     with Session(bind=self.db_engine) as session:
    #         try:
    #             # Retrieve the knowledge base DTO
    #             knowledge_base_dto = session.query(KnowledgeBaseDTO).filter_by(user_id=user_id, kb_id=kb_id).first()
    #             if not knowledge_base_dto:
    #                 raise Exception(f"KnowledgeBase with user_id {user_id} and kb_id {kb_id} not found.")
    #
    #             # Create a new PdfDocumentDTO
    #             # pdf_doc_dto = map_domain_to_pdf_document_dto(pdf_doc)
    #
    #             # Add the new PDF document to the session and commit it
    #             session.add(pdf_doc_dto)
    #             session.commit()
    #             print(f"Document '{pdf_doc.doc_name}' added successfully to KnowledgeBase {kb_id} for user {user_id}")
    #
    #         except Exception as e:
    #             session.rollback()  # Rollback the transaction in case of any error
    #             print(f"Error adding PDF document: {e}")
    #             raise


def map_knowledge_base_dto_to_domain(knowledge_base_dto: Type[KnowledgeBaseDTO]) -> KnowledgeBase:
    doc_ids = [doc.doc_id for doc in knowledge_base_dto.pdf_documents]
    return KnowledgeBase(
        user_id=knowledge_base_dto.user_id,
        kb_id=knowledge_base_dto.kb_id,
        kb_name=knowledge_base_dto.kb_name,
        doc_ids=doc_ids,
        bm25_index_location=knowledge_base_dto.bm25_index_location
    )


# def map_domain_to_pdf_document_dto(pdf_doc: PdfDocument) -> PdfDocumentDTO:
#     return PdfDocumentDTO(
#         doc_id=pdf_doc.doc_id,
#         user_id=pdf_doc.username,
#         kb_id=pdf_doc.kb_name,
#         document_name=pdf_doc.document_name,
#         source=pdf_doc.source,
#         raw_location=pdf_doc.raw_location,
#         chunked_location=pdf_doc.chunked_location
#     )
