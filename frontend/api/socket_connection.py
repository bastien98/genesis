import socketio
from fastapi.applications import ASGIApp
from os import environ as prior_environ
from dotenv import load_dotenv

load_dotenv()


def handle_connect(sid, environ):
    print(sid)


class SocketManager:
    def __init__(self, origins: list[str]):
        self.server = socketio.AsyncServer(
            cors_allowed_origins=origins,
            async_mode="asgi",
            logger=True,
            engineio_logger=True,
        )
        self.app = socketio.ASGIApp(self.server)

    @property
    def on(self):
        return self.server.on

    @property
    def send(self):
        return self.server.send

    def mount_to(self, path: str, app: ASGIApp):
        app.mount(path, self.app)


socket_manager = SocketManager([prior_environ.get("CLIENT_URL")])
socket_manager.on("connect", handler=handle_connect)
