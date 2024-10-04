from abc import ABC, abstractmethod

from file_api_v2.domain.entities.user import User


class UsersPort(ABC):

    @abstractmethod
    def retrieve_user(self, username: str) -> User:
        pass
