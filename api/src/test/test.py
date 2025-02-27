from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

from domain.entities.message import Message
from domain.entities.thread import Thread
from infra.mysql.adapters.mysql_chat_adapter import MySQLChatAdapter
from infra.mysql.dtos import Base  # Make sure this points to your declarative_base


def main():
    # Replace 'user' and 'password' with your MySQL credentials.
    DATABASE_URL = "mysql+mysqlconnector://root:Gilles1998@localhost/genesis"

    # Create the SQLAlchemy engine and session
    engine = create_engine(DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Create tables if they do not exist
    Base.metadata.create_all(bind=engine)

    # Instantiate the chat adapter
    chat_adapter = MySQLChatAdapter(session)

    # Create a new chat thread (this is required to add messages)
    new_thread = Thread(user_id=1)
    chat_adapter.add_thread(new_thread)
    print(f"Created thread with ID: {new_thread.thread_id}")

    # Create a new message for the thread
    new_message = Message(
        thread_id=2,
        user_id=1,
        message="Hello, this is a test message! 2"
    )
    chat_adapter.add_message(new_message)
    print(f"Added message with ID: {new_message.message_id}")

    # Retrieve all messages for the thread using get_messages_by_thread
    messages = chat_adapter.get_messages_by_thread(2)
    print("Retrieved messages for the thread:")
    for msg in messages:
        print(msg)

    # Optionally, close the session when done
    session.close()


if __name__ == '__main__':
    main()
