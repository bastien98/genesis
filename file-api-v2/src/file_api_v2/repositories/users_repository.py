from file_api_v2.domain.entities.user import User
from file_api_v2.ports.user_port import UsersPort


class UsersRepository:
    def __init__(self, users: UsersPort):
        self.users = users

    def retrieve_user(self, username: str) -> User:
        user = self.users.retrieve_user(username)
        if user is None:
            # Raise a custom exception if the user is not found
            raise UserNotFoundException(username)
        return user

    def persist_user(self, user: User) -> None:
        return self.users.update_user(user)



class UserNotFoundException(Exception):
    """Exception raised when a User is not found."""
    def __init__(self, username: str):
        super().__init__(f"User with username '{username}' not found.")
        self.username = username