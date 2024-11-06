from fastapi import FastAPI
from dummy_data import chats, knowledge_bases, chat_messages
from models import NewChatRequestBody, NewMessageRequestBody
import time
from socket_connection import socket_manager
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
origins = [environ.get("CLIENT_URL")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
socket_manager.mount_to("/chat", app)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/get_chats")
def get_chats():
    return chats


@app.get("/get_knowledge_bases")
def get_knowledge_bases():
    return knowledge_bases


@app.get("/delete_chat/{chat_id}")
def delete_chat(chat_id: int):
    for chat in chats:
        if chat["id"] == chat_id:
            chats.remove(chat)
            break

    for message in chat_messages:
        if message["chat_id"] == chat_id:
            chat_messages.remove(message)

    return {
        "chats": chats,
        "chat_messages": chat_messages,
    }


@app.get("/get_chat_messages/{chat_id}")
def get_chat_messages(chat_id: int):
    messages = []

    if len(chats) > 0 and len(chat_messages) > 0:
        for chat in chats:
            if chat["id"] == chat_id:
                for message in chat_messages:
                    if message["chat_id"] == chat_id:
                        messages.append(message)
                break

        return messages

    return messages


@app.post("/new_chat")
def new_chat(new_chat_request_body: NewChatRequestBody):
    chats.append(
        {
            "id": len(chats) + 1,
            "title": new_chat_request_body.user_message,
            "time_category": "Today",
            "updated_at": time.time(),
            "knowledge_base": new_chat_request_body.knowledge_base,
        }
    )

    chat_messages.append(
        {
            "id": len(chat_messages) + 1,
            "chat_id": len(chats),
            "text": new_chat_request_body.user_message,
            "message_from": "User",
            "sent_at": time.time(),
        }
    )

    return {
        "chats": chats,
        "chat_messages": chat_messages,
    }


@app.post("/new_message")
def new_message(new_message_request_body: NewMessageRequestBody):
    chat_messages.append(
        {
            "id": len(chat_messages) + 1,
            "chat_id": new_message_request_body.chat_id,
            "text": new_message_request_body.user_message,
            "message_from": "User",
            "sent_at": time.time(),
        }
    )

    return {
        "chat_messages": chat_messages,
    }


@app.get("/get_profile")
def get_profile():
    return {"username": "syedmsannan", "image": "/static/image.png"}
