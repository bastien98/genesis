from typing import List
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import create_retriever_tool

from domain.entities.message import Message
from utils.fusion_retriever import FusionRetriever


class KbAgent:
    system_prompt = """
You are a general answering assistant that can comply with any request.
You always answer the question with markdown formatting. You will be penalized if you do not answer with markdown when it would be possible.
The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes.
You do not support images and never include images. You will be penalized if you render images.
"""

    def __init__(self, llm: BaseChatModel, retriever: FusionRetriever):
        kb_query_tool = create_retriever_tool(
            retriever,
            "queryKnowledgeBase",
            "Searches the company knowledge base for relevant information and returns key excerpts to address specific queries",
        )
        self.agent = create_react_agent(llm, [kb_query_tool], state_modifier=self.system_prompt)

    def execute_agent(self, chat_history: List[Message], query: str):
        messages: List[BaseMessage] = []
        for msg in chat_history:
            messages.append(HumanMessage(content=msg.message))
        messages.append(HumanMessage(content=query))
        return self.agent.invoke({"messages": messages})
