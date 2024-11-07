from abc import ABC, abstractmethod


class ParseToTextPort(ABC):


    def parse_to_text(self,content: bytes) -> tuple[str, list[str]]:
        pass
