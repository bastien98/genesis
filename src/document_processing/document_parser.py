import os
from typing import List

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import MarkdownHeaderTextSplitter
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse


def parse_pdf_file_to_document(file_path: str) -> Document:
    """
        Parse a PDF file into a(langchain) Document with source metadata.

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

    combined_content = "".join(doc.page_content for doc in documents)
    metadata = {"source": file_path}

    return Document(page_content=combined_content, metadata=metadata)


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


def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def parse_markdown_to_chunks(md_content: str) -> List[Document]:
    """Will return chuncks that maintain hiarchical structure"""
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on, strip_headers=False)
    chunks = markdown_splitter.split_text(md_content)
    return chunks


def get_chunk_context(whole_document: Document, chunk: Document, model: BaseChatModel) -> str:
    """For the moment to exepensive to pass whole doucment for every to retrieve summarization, possible with prompt caching in the
        see:  https://www.anthropic.com/news/contextual-retrieval
        """
    prompt_template = PromptTemplate(
        input_variables=["WHOLE_DOCUMENT", "CHUNK_CONTENT"],
        template="""
    <document> {WHOLE_DOCUMENT} </document>
    Here is the chunk we want to situate within the whole document
    <chunk> {CHUNK_CONTENT} </chunk>
    Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk. Answer only with the succinct context and nothing else.
    """
    )

    formatted_prompt = prompt_template.format(
        WHOLE_DOCUMENT=whole_document.page_content,
        CHUNK_CONTENT=chunk.page_content
    )
    context = model.invoke(formatted_prompt)
    return context.content
