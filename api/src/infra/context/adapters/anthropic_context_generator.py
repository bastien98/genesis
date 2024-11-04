from anthropic import AsyncAnthropic, BaseModel
from instructor import AsyncInstructor, patch, Mode
from pydantic import Field

from ports.context_model_port import ContextGeneratorPort

class SituatedContext(BaseModel):
    title: str = Field(..., description="The title of the document.")
    context: str = Field(..., description="The context to situate the chunk within the document.")

class AnthropicAdapter(ContextGeneratorPort):
    def __init__(self, client: AsyncInstructor):
        self.client = client


    async def generate_context(self, doc: str, chunk: str) -> str:
        response = await self.client.chat.completions.create(
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
                            "text": "Here is the chunk we want to situate within the whole document\n<chunk>{{"
                                    "chunk}}</chunk>\nPlease give a short succinct context to situate this chunk "
                                    "within the overall document for the purposes of improving search retrieval of "
                                    "the chunk.\nAnswer only with the succinct context and nothing else.",
                        },
                    ],
                }
            ],
            response_model=SituatedContext,
            context={"doc": doc, "chunk": chunk},
        )
        return response.context


AsyncInstructor(
                                        client=AsyncAnthropic(),
                                        create=patch(
                                            create=AsyncAnthropic().beta.prompt_caching.messages.create,
                                            mode=Mode.ANTHROPIC_TOOLS,
                                        ),
                                        mode=Mode.ANTHROPIC_TOOLS,
                                    )
