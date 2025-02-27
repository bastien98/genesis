from typing import List, Optional
from domain.entities.message import Message


class Thread:
    def __init__(
            self,
            thread_id: Optional[int] = None,
            user_id: int = None,
            messages: Optional[List["Message"]] = None
    ):
        self.thread_id = thread_id
        self.user_id = user_id
        self.messages = messages or []

    def __repr__(self):
        return (
            f"<Thread(thread_id={self.thread_id}, user_id={self.user_id}, "
            f"messages={self.messages})>"
        )
