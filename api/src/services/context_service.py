import asyncio
from abc import ABC
from typing import List, Dict

from pydantic import BaseModel, Field

from ports.context_model_port import ContextGeneratorPort


class ContextService:

    def __init__(self, context_generator_adapter: ContextGeneratorPort):
        self.context_generator = context_generator_adapter

    async def generate_context(self, doc: str, chunk: str) :
        context = await self.context_generator.generate_context(doc=doc, chunk=chunk)
        return context

    async def process_chunk(self, doc: str, chunk: str) -> Dict[str, str]:
        context = await self.generate_context(doc, chunk)
        return {
            "chunk": chunk,
            "context": context
        }

    async def add_context_to_chunks(self, doc: str, chunks: List[str]) -> List[Dict[str, str]]:
        semaphore = asyncio.Semaphore(3)

        async def limited_process_chunk(doc: str, chunk: str):
            async with semaphore:
                return await self.process_chunk(doc, chunk)

        tasks = [limited_process_chunk(doc, chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
        return results

    async def create_context_chunks(self, doc: str, chunks: List[str]) -> list[str]:
        processed_chunks = await self.add_context_to_chunks(doc, chunks)
        output = []

        for i, item in enumerate(processed_chunks):
            chunk_str = (
                f"Chunk {i + 1}:\n"
                f"Context: {item['context']}\n"
                f"Text: {item['chunk']}\n"
            )
            output.append(chunk_str)

        return output
