from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import BaseNode


def parse_md_files(dir_path: str) -> List[BaseNode]:
    markdown_parser = MarkdownNodeParser()
    documents = SimpleDirectoryReader(dir_path).load_data()
    nodes = markdown_parser.get_nodes_from_documents(documents)
    return nodes

