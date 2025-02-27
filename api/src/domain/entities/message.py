from datetime import datetime
from typing import List, Optional


class Message:
    def __init__(
            self,
            message_id: Optional[int] = None,
            thread_id: int = None,
            user_id: int = None,
            message: str = "",
            created_at: Optional[datetime] = None

    ):
        self.message_id = message_id
        self.thread_id = thread_id
        self.user_id = user_id
        self.message = message
        self.created_at = created_at

    def __repr__(self):
        return (
            f"<Message(message_id={self.message_id}, thread_id={self.thread_id}, "
            f"user_id={self.user_id}, message={self.message})>"
        )
