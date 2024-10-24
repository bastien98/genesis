from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> None:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass
