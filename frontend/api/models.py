from pydantic import BaseModel


class NewChatRequestBody(BaseModel):
    user_message: str
    knowledge_base: str


class NewMessageRequestBody(BaseModel):
    user_message: str
    chat_id: str
