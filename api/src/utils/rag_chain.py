from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable


class RagChain:
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Keep the answer concise."
        "\n\n"
        "{context}"
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    def __init__(self, llm: BaseChatModel):
        self.llm = llm

    def create_rag_chain(self, retriever: BaseRetriever) -> Runnable:
        question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        return create_retrieval_chain(retriever, question_answer_chain)
