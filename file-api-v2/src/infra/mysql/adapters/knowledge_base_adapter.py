from typing import Type

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from file_api_v2.ports.knowledge_base_port import KnowledgeBasePort
from infra.mysql.dtos import KnowledgeBaseDTO


class KnowledgeBaseAdapter(KnowledgeBasePort):
    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    def retrieve_knowledge_base(self, user_id: int, kb_id: int) -> KnowledgeBaseDTO:
        with Session(bind=self.db_engine) as session:
            try:
                # Query the database for the KnowledgeBase object
                knowledge_base = session.query(KnowledgeBaseDTO).filter_by(user_id=user_id, kb_id=kb_id).first()

                if not knowledge_base:
                    raise Exception(f"KnowledgeBase with user_id {user_id} and kb_id {kb_id} not found.")

                return knowledge_base

            except Exception as e:
                print(f"Error retrieving KnowledgeBase: {e}")
                raise
