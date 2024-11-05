from ollama import AsyncClient

from ports.context_generator_port import ContextGeneratorPort


class OllamaContextAdapter(ContextGeneratorPort):
    def __init__(self, client : AsyncClient):
        self.client = client

    async def generate_context(self, doc: str, chunk: str) -> str:
        prompt = f"""<document>{doc}</document>
                    Here is the chunk we want to situate within the whole document <chunk>{chunk}</chunk>
                    Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
                    Answer only with the succinct context and nothing else."""

        response = await self.client.generate(model="llama3.2", prompt=prompt)
        context = response.get("response")
        return context
