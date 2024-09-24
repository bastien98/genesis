from dotenv import load_dotenv

from src.document_processing.document_parser import parse_pdf_file_to_documents

load_dotenv()

parse_pdf_file_to_documents("data/raw/pdf/dbt-exam-full.pdf")