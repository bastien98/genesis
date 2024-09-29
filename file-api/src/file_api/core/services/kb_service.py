from file_api.core.ports.file_storage_port import FileStoragePort
from file_api.core.ports.indexing_port import BM25IndexingStrategy


class KBService:
    def __init__(self, file_storage: FileStoragePort, bm25_index_creator: BM25IndexingStrategy):
        self.file_storage = file_storage
        self.create_bm25_index = bm25_index_creator

    async def update(self, filename: str) -> None:
        await self._update_BM25_index(filename)

    async def _update_BM25_index(self, filename: str) -> None:
        documents = await self.file_storage.read_directory(
            self.file_storage.get_clean_output_location(filename).get_directory_location)
        bm25_index = self.create_bm25_index(documents)
        await self.file_storage.save_BM25_index(bm25_index, filename)
