from file_api.core.domain.embeddings_model import Embeddings
from file_api.core.ports.vector_db_port import VectorDbPort


class LocalVectorDbAdapter(VectorDbPort):
    async def save_embeddings(self, embeddings: Embeddings, vector_db_index: str) -> None:
        pass