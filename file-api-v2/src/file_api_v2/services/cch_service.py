import asyncio
from typing import List, Dict

from anthropic import AsyncAnthropic
from instructor import AsyncInstructor, patch, Mode
from pydantic import BaseModel, Field


class SituatedContext(BaseModel):
    title: str = Field(..., description="The title of the document.")
    context: str = Field(..., description="The context to situate the chunk within the document.")


client = AsyncInstructor(
    client=AsyncAnthropic(),
    create=patch(
        create=AsyncAnthropic().beta.prompt_caching.messages.create,
        mode=Mode.ANTHROPIC_TOOLS,
    ),
    mode=Mode.ANTHROPIC_TOOLS,
)


async def situate_context(doc: str, chunk: str) -> str:
    response = await client.chat.completions.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0.0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "<document>{{doc}}</document>",
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": "Here is the chunk we want to situate within the whole document\n<chunk>{{chunk}}</chunk>\nPlease give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.\nAnswer only with the succinct context and nothing else.",
                    },
                ],
            }
        ],
        response_model=SituatedContext,
        context={"doc": doc, "chunk": chunk},
    )
    return response.context


async def process_chunk(doc: str, chunk: str) -> Dict[str, str]:
    context = await situate_context(doc, chunk)
    return {
        "chunk": chunk,
        "context": context
    }


async def add_context_to_chunks(doc: str, chunks: List[str]) -> List[Dict[str, str]]:
    semaphore = asyncio.Semaphore(3)

    async def limited_process_chunk(doc: str, chunk: str):
        async with semaphore:
            return await process_chunk(doc, chunk)

    tasks = [limited_process_chunk(doc, chunk) for chunk in chunks]
    results = await asyncio.gather(*tasks)
    return results


async def create_context_chunks(doc: str, chunks: List[str]) -> list[str]:
    processed_chunks = await add_context_to_chunks(doc, chunks)
    output = []

    for i, item in enumerate(processed_chunks):
        chunk_str = (
            f"Chunk {i + 1}:\n"
            f"Context: {item['context']}\n"
            f"Text: {item['chunk']}\n"
        )
        output.append(chunk_str)

    return output
