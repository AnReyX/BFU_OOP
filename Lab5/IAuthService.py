from abc import ABC, abstractmethod
from typing import Optional
from User import User

class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, login: str, password: str) -> None:
        pass

    @abstractmethod
    def sign_out(self) -> None:
        pass

    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    @abstractmethod
    def current_user(self) -> Optional[User]:
        pass