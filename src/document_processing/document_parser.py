import os
from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.schema import Document, BaseNode
from llama_parse import LlamaParse


def parse_pdf_file_to_documents(file_path: str) -> List[Document]:
    """
        Parse a PDF file into a list of Document objects using LlamaParse.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            List[Document]: List of Document objects, each representing a page from the PDF in markdown format.
        """
    parser = LlamaParse(
        do_not_unroll_columns=True,  # new llms understand spatial layout
        result_type="markdown",
        language="en",
        # check https://github.com/run-llama/llama_parse/blob/main/llama_parse/utils.py#L16 for other language support (default english)
    )
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[file_path],
                                      file_extractor=file_extractor).load_data()
    return documents


def save_documents_as_markdown(documents: List[Document], output_dir: str, filename: str) -> None:
    """
    Save a list of Document objects as a single markdown file.

    Args:
        documents (List[Document]): List of Document objects to save.
        output_dir (str): Directory where the markdown file will be saved.
        filename (str): Name of the output markdown file.

    Returns:
        None
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Ensure the filename has a .md extension
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding='utf-8') as f:
        for i, doc in enumerate(documents):
            if i > 0:  # Add separator for all pages except the first
                f.write("---\n")
            f.write(doc.text + '\n\n')

    print(f"Saved {len(documents)} documents as '{filename}' in {output_dir}")


def parse_markdown_to_nodes(file_path: str) -> List[BaseNode]:
    """
        Parse a Markdown file into LlamaIndex BaseNodes using MarkdownNodeParser defaults.

        Args:
            file_path (str): Path to the Markdown file.

        Returns:
            List[BaseNode]: Parsed segments of the Markdown document.
        """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    markdown_parser = MarkdownNodeParser()
    nodes = markdown_parser.get_nodes_from_documents([Document(text=content)])
    return nodes
