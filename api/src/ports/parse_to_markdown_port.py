from abc import ABC, abstractmethod
from api.src.domain.entities.raw_document import RawDocument


class ParseToMarkdownPort(ABC):

    @abstractmethod
    async def parse_to_markdown(self, doc: RawDocument) -> tuple[str, list[str]]:#(full markdown string, chunked markdown str list)
        pass
