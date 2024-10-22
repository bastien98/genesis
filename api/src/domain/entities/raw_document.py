from dataclasses import dataclass


@dataclass
class RawDocument:
    name: str
    source: str
    content: bytes
