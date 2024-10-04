from file_api_v2.domain.entities.user import User
from file_api_v2.ports.user_port import UsersPort


class UsersRepository:
    def __init__(self, users: UsersPort):
        self.users = users

    def retrieve_user(self, username: str) -> User:
        return self.users.retrieve_user(username)

    def persist_user(self, user: User) -> None:
        return self.users.update_user(user)
