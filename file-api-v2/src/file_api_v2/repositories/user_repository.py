from file_api_v2.domain.entities.user import User
from file_api_v2.ports.user_port import UsersPort


class UserRepository:
    def __init__(self, users: UsersPort):
        self.users = users

    def retrieve_user(self, username: str) -> User:
        """Retrieve a user by username, raise an exception if not found."""
        try:
            user = self.users.retrieve_user(username)
            if user is None:
                raise UserNotFoundException(username)
            return user
        except Exception as e:
            raise UserNotFoundException(username) from e

    def persist_user(self, user: User) -> None:
        """Persist the user to the repository, raise an exception if it fails."""
        try:
            self.users.update_user(user)
        except Exception as e:
            raise UserPersistenceException(user, message="Failed to update user") from e


class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found.")


class UserPersistenceException(Exception):
    """Exception raised when there is an error persisting the user."""

    def __init__(self, user: User, message: str = "Error persisting user"):
        super().__init__(f"{message}: {user.username}")
