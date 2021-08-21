from abc import ABC, abstractmethod


class AuthenticationService(ABC):

    @abstractmethod
    def is_a_valid_user(self, username, password) -> bool:
        pass