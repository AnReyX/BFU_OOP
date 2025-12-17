from DataRepository import DataRepository
from User import User
from pathlib import Path
import json

class UserRepository(DataRepository[User]):
    def __init__(self, rep_path):
        super().__init__(rep_path, User)

    def get_by_login(self, login: str) -> User | None:
        data = self.get_all()

        for element in data:
            if element.login == login:
                return element
        
        return None