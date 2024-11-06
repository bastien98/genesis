from abc import ABC, abstractmethod

class ContextGeneratorPort(ABC):

    @abstractmethod
    async def generate_context(self, doc: str, chunk: str) -> str:
        """Generate a succinct context for a given document and chunk."""