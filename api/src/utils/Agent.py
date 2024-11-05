from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import create_retriever_tool
from langgraph.checkpoint.memory import MemorySaver

from utils.fusion_retriever import FusionRetriever


class KbAgent:

    def __init__(self, llm: BaseChatModel, retriever: FusionRetriever):
        self.retriever = retriever
        self.llm = llm
        tool = create_retriever_tool(
            retriever,
            "queryKnowledgeBase",
            "Searches the company knowledge base for relevant information and returns key excerpts to address specific queries",
        )
        self.tools = [tool]
        memory = MemorySaver()
        self.agent = create_react_agent(llm, self.tools, state_modifier="""
 You are a general answering assistant that can comply with any request.
You always answer the with markdown formatting. You will be penalized if you do not answer with markdown when it would be possible.
The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, and blockquotes.
You do not support images and never include images. You will be penalized if you render images.
        """)

    def execute_agent(self, query: str):
        return self.agent.invoke({"messages": [HumanMessage(content=query)]},
                                 config={"configurable": {"thread_id": "3"}})
