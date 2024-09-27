from langchain_core.documents import Document
from llama_parse import LlamaParse

from file_api.core.ports.file_parser_port import FileParserPort
from file_api.core.ports.file_storage_port import FileLocation


class LlamaParser(FileParserPort):

    async def parse_to_clean_document(self, file_location: FileLocation) -> Document:
        parser = LlamaParse(
            result_type="markdown"
        )

        llama_documents = await parser.aload_data(file_location.full_path)
        combined_text = ""
        for doc in llama_documents:
            combined_text += doc.text + "\n"
        langchain_doc = Document(page_content=combined_text.strip())
        return langchain_doc
