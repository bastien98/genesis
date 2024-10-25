from typing import Optional
from domain.entities.user import User
from ports.user_repository_port import UserRepositoryPort


class UserRepository:
    def __init__(self, user_repo_adapter: UserRepositoryPort):
        self.user_repo_adapter = user_repo_adapter

    def get_by_username(self, username: str) -> Optional[User]:
        return self.user_repo_adapter.get_by_username(username)

    def get_by_user_id(self, user_id: int) -> Optional[User]:
        return self.user_repo_adapter.get_by_user_id(user_id)

    def update(self, user: User) -> None:
        self.user_repo_adapter.update(user)




class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, username: str):
        super().__init__(f"User '{username}' not found.")


class UserPersistenceException(Exception):
    """Exception raised when there is an error persisting the user."""

    def __init__(self, user: User, message: str = "Error persisting user"):
        super().__init__(f"{message}: {user.username}")
