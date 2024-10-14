from typing import List

from file_api_v2.utils.parser import Parser


class Chunker:
    @staticmethod
    def chunk_content(content: str) -> List[str]:
        delimiter = Parser.PAGE_DELIMITER
        chunks = content.split(delimiter)
        return chunks
