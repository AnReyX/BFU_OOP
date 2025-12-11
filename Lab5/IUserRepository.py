from IDataRepository import IDataRepository
from User import User

class IUserRepository(IDataRepository[User]):
    def get_by_login(self, login: str) -> User | None:
        ...