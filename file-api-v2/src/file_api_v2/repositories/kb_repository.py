class KbRepository:
    def __init__(self, vector_db_adapter: VectorDbPort, document_storage_adapter: DocumentStoragePort,
                 knowledge_base_adapter: KnowledgeBasePort):
        self.vector_db_adapter = vector_db_adapter
        self.document_storage_adapter = document_storage_adapter
        self.knowledge_base_adapter = knowledge_base_adapter

    def retrieve_knowledge_base(self, user_id, kb_id):
        return self.knowledge_base_adapter.retrieve_knowledge_base(user_id, kb_id)
