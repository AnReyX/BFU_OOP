from DataRepository import DataRepository
from User import User
from IUserRepository import IUserRepository
from typing import Optional

class UserRepository(DataRepository[User], IUserRepository):
    """
    Конкретный репозиторий для User.
    Передает класс User в родительский DataRepository.
    """

    def __init__(self, filename: str):
        super().__init__(filename, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for user in self.get_all():
            if user.login == login:
                return user
        return None