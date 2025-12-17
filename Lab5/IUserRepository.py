from IDataRepository import IDataRepository
from User import User
from abc import abstractmethod
from typing import Optional

class IUserRepository(IDataRepository[User]):
    @abstractmethod
    def get_by_login(self, login: str) -> Optional[User]:
        pass