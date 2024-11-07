
from llama_parse import LlamaParse
from api.src.domain.entities.raw_document import RawDocument
from api.src.ports.parse_to_markdown_port import ParseToMarkdownPort


class MineruAdapter(ParseToMarkdownPort):


    async def parse_to_markdown(self, doc: RawDocument) -> tuple[str, list[str]]:
        parser = LlamaParse(
            result_type="markdown"
        )
        llama_documents = await parser.aload_data(doc.content, extra_info={'file_name': doc.name})
        print("Parsing to markdown finished")
        pages = [page.text for page in llama_documents]

        return "\n".join(pages), pages