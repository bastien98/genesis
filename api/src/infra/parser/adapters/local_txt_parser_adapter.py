
from llama_parse import LlamaParse
from api.src.domain.entities.raw_document import RawDocument
from api.src.ports.parse_to_text_port import ParseToTextPort


class LocalTxtParserAdapter(ParseToTextPort):

    def parse_to_text(self, content: bytes) -> tuple[str, list[str]]:

        return "", ["e","e"]