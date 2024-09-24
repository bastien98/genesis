import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.document_processing.document_parser import read_markdown_file, parse_markdown_to_chunks, get_chunk_context

load_dotenv()
MD_FILE_PATH = "./data/processed/markdown/dbt-exam-full/dbt-exam-full.md"
# Do not run, costs money
# documents = parse_pdf_file_to_documents("data/raw/pdf/dbt-exam-full.pdf")
# save_documents_as_markdown(documents, "./data/processed/markdown/dbt-exam-full", "dbt-exam-full")
# documents = split_markdownd_by_header("./data/processed/markdown/dbt-exam-full/dbt-exam-full.md")


content = read_markdown_file(MD_FILE_PATH)
chunks = parse_markdown_to_chunks(content)
get_chunk_context(Document(page_content=content), chunks[0], ChatOpenAI(model="gpt-3.5-turbo-0125")),