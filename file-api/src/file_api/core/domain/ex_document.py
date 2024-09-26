from dataclasses import dataclass


@dataclass
class ExDocument:
    name: str
    content: bytes

    def __str__(self) -> str:
        return f"Document(name='{self.name})"
