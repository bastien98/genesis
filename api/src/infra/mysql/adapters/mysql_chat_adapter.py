from sqlalchemy.orm import Session
from typing import Optional, List
from domain.entities.message import Message
from domain.entities.thread import Thread
from infra.mysql.dtos import ThreadDTO, MessageDTO
from sqlalchemy import asc


class MySQLChatAdapter:
    def __init__(self, session: Session):
        self.session = session

    # ----- Thread Methods -----
    def add_thread(self, thread: Thread) -> None:
        """
        Add a new chat thread to the database.
        After commit, the thread's id is updated.
        """
        thread_dto = ThreadDTO(user_id=thread.user_id)
        self.session.add(thread_dto)
        self.session.commit()
        thread.thread_id = thread_dto.thread_id

    def get_thread_by_id(self, thread_id: int) -> Optional[Thread]:
        """
        Retrieve a chat thread by its ID, including its messages.
        """
        thread_dto = self.session.query(ThreadDTO).filter_by(thread_id=thread_id).first()
        if thread_dto is None:
            return None

        # Convert associated messages from DTOs to domain entities.
        messages = []
        for msg_dto in thread_dto.messages:
            message = Message(
                message_id=msg_dto.message_id,
                thread_id=msg_dto.thread_id,
                user_id=msg_dto.user_id,
                message=msg_dto.message,
                created_at=msg_dto.created_at
            )
            messages.append(message)

        thread = Thread(
            thread_id=thread_dto.thread_id,
            user_id=thread_dto.user_id,
            messages=messages
        )
        return thread

    def get_threads_by_user_id(self, user_id: int) -> List[Thread]:
        """
        Retrieve all chat threads for a given user.
        """
        thread_dtos = self.session.query(ThreadDTO).filter_by(user_id=user_id).all()
        threads = []
        for thread_dto in thread_dtos:
            messages = []
            for msg_dto in thread_dto.messages:
                message = Message(
                    message_id=msg_dto.message_id,
                    thread_id=msg_dto.thread_id,
                    user_id=msg_dto.user_id,
                    message=msg_dto.message,
                    created_at=msg_dto.created_at
                )
                messages.append(message)
            thread = Thread(
                thread_id=thread_dto.thread_id,
                user_id=thread_dto.user_id,
                messages=messages
            )
            threads.append(thread)
        return threads

    def update_thread(self, thread: Thread) -> None:
        """
        Update an existing chat thread.
        """
        thread_dto = self.session.query(ThreadDTO).filter_by(thread_id=thread.thread_id).first()
        if thread_dto is None:
            raise Exception(f"Thread with id '{thread.thread_id}' not found")
        self.session.commit()

    def delete_thread(self, thread: Thread) -> None:
        """
        Delete a chat thread (and all associated messages due to cascade).
        """
        thread_dto = self.session.query(ThreadDTO).filter_by(thread_id=thread.thread_id).first()
        if thread_dto is None:
            raise Exception(f"Thread with id '{thread.thread_id}' not found")
        self.session.delete(thread_dto)
        self.session.commit()

    # ----- Message Methods -----
    def add_message(self, message: Message) -> Message:
        """
        Add a new message to a thread.
        After commit, the message's id is updated.
        """
        message_dto = MessageDTO(
            thread_id=message.thread_id,
            user_id=message.user_id,
            message=message.message
        )
        self.session.add(message_dto)
        self.session.commit()
        return Message(user_id=message.user_id, thread_id=message.thread_id, message_id=message.message_id)

    def get_message_by_id(self, message_id: int) -> Optional[Message]:
        """
        Retrieve a message by its id.
        """
        msg_dto = self.session.query(MessageDTO).filter_by(message_id=message_id).first()
        if msg_dto is None:
            return None
        return Message(
            message_id=msg_dto.message_id,
            thread_id=msg_dto.thread_id,
            user_id=msg_dto.user_id,
            message=msg_dto.message,
            created_at=msg_dto.created_at
        )

    def get_messages_by_thread(self, thread_id: int) -> List[Message]:
        """
        Retrieve all messages for a specific thread, ordered by creation time.
        """
        msg_dtos = self.session.query(MessageDTO).filter_by(thread_id=thread_id).order_by(
            MessageDTO.created_at.asc()).all()
        messages = []
        for msg_dto in msg_dtos:
            message = Message(
                message_id=msg_dto.message_id,
                thread_id=msg_dto.thread_id,
                user_id=msg_dto.user_id,
                message=msg_dto.message,
                created_at=msg_dto.created_at
            )
            messages.append(message)
        return messages

    def update_message(self, message: Message) -> None:
        """
        Update an existing message.
        """
        msg_dto = self.session.query(MessageDTO).filter_by(message_id=message.message_id).first()
        if msg_dto is None:
            raise Exception(f"Message with id '{message.message_id}' not found")
        msg_dto.message = message.message
        self.session.commit()

    def delete_message(self, message: Message) -> None:
        """
        Delete a message.
        """
        msg_dto = self.session.query(MessageDTO).filter_by(message_id=message.message_id).first()
        if msg_dto is None:
            raise Exception(f"Message with id '{message.message_id}' not found")
        self.session.delete(msg_dto)
        self.session.commit()
