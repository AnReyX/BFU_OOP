from User import User
from abc import ABC, abstractmethod


class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, user: User) -> None:
        ...
    
    @abstractmethod
    def sign_out(self, user: User) -> None:
        ...
    
    @abstractmethod
    def is_authorized(self, user: User) -> bool:
        ...
    
    @abstractmethod
    def current_user(self, user: User) -> None:
        ...