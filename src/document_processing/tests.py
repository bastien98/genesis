from dotenv import load_dotenv

from src.document_processing.document_parser import parse_pdf_file_to_documents, save_documents_as_markdown, \
    parse_markdown_to_nodes

load_dotenv()
# Do not run, costs money
# documents = parse_pdf_file_to_documents("data/raw/pdf/dbt-exam-full.pdf")
# save_documents_as_markdown(documents, "./data/processed/markdown/dbt-exam-full", "dbt-exam-full")
documents = parse_markdown_to_nodes("./data/processed/markdown/dbt-exam-full/dbt-exam-full.md")
pass