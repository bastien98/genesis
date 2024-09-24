from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document
from llama_parse import LlamaParse


def parse_pdf_file_to_documents(file_path: str) -> List[Document]:
    """
        Parse a PDF file into a list of Document objects.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            List[Document]: List of Document objects, each representing a page from the PDF in markdown format.
        """
    parser = LlamaParse(
        result_type="markdown"
    )
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[file_path],
                                      file_extractor=file_extractor).load_data()
    return documents
