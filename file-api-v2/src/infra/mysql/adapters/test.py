from sqlalchemy import create_engine

from infra.mysql.adapters.knowledge_base_adapter import KnowledgeBaseAdapter

engine = create_engine("mysql+mysqlconnector://root:Gilles1998@localhost/superRag")
adapter = KnowledgeBaseAdapter(engine)

try:
    kb = adapter.retrieve_knowledge_base(user_id=1, kb_id=1)
    print(f"Knowledge Base: {kb.kb_name}, BM25 Index Location: {kb.bm25_index_location}")
except Exception as e:
    print(e)
