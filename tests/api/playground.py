import os

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from domain.entities.message import Message
from domain.entities.thread import Thread
from infra.mysql.adapters.mysql_chat_adapter import MySQLChatAdapter
from infra.mysql.dtos import Base


def main():
    DATABASE_URL = os.getenv("DB_CONN")

    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    Base.metadata.create_all(bind=engine)

    chat_adapter = MySQLChatAdapter(session)

    new_thread = Thread(user_id=1)
    chat_adapter.add_thread(new_thread)
    print(f"Created thread with ID: {new_thread.thread_id}")

    new_message = Message(
        thread_id=2,
        user_id=1,
        message="Hello, this is a test message! 2"
    )
    chat_adapter.add_message(new_message)
    print(f"Added message with ID: {new_message.message_id}")

    messages = chat_adapter.get_messages_by_thread(2)
    print("Retrieved messages for the thread:")
    for msg in messages:
        print(msg)

    session.close()


if __name__ == '__main__':
    main()
