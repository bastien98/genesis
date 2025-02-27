import re
from typing import List
from rank_bm25 import BM25Okapi
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import multiprocessing
import os
import pickle
import logging
from domain.entities.knowledge_base import KnowledgeBase
from domain.entities.message import Message
from infra.mysql.adapters.mysql_chat_adapter import MySQLChatAdapter
from services.file_storage_service import FileStorageService
from services.location_service import LocationService


class ChatService:
    def __init__(self, chat_adapter: MySQLChatAdapter):
        self.chatAdapter = chat_adapter

    def add_message(self, message: Message) -> Message:
        return self.chatAdapter.add_message(message)

    def get_messages_by_thread(self, thread_id: int) -> List[Message]:
        return self.chatAdapter.get_messages_by_thread(thread_id=thread_id)
