from io import BytesIO

import PyPDF2
from fastapi import UploadFile
from langchain_core.documents import Document


async def uploadFile_mapper(file: UploadFile, source: str) -> Document:
    contents = await file.read()
    reader = PyPDF2.PdfReader(BytesIO(contents))

    full_text = ""
    # Iterate over all the pages in the PDF
    for page_number in range(len(reader.pages)):
        page = reader.pages[page_number]
        text = page.extract_text()
        full_text += text

    document = Document(page_content=full_text, metadata={"source": source, "file_name": file.filename})
    return document
