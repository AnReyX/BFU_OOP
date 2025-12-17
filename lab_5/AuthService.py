from IAuthService import IAuthService
from User import User
import json
from UserRepository import UserRepository

CURENT_USER_FILE_PATH = "labs/lab_5/current_user.json"


class AuthService(IAuthService):
    def __init__(self, signedin_users_repository: UserRepository, signedout_users_repository: UserRepository) -> None:
        self._auth_users_repository = signedin_users_repository
        self._not_auth_users_repository = signedout_users_repository

    def sign_in(self, user: User) -> None:
        if self._auth_users_repository.get_by_id(user.id) != None or self._not_auth_users_repository.get_by_id(user.id) == None:
            return

        if self._not_auth_users_repository.get_by_id(user.id) != None:
            self._not_auth_users_repository.delete(user)

        self._auth_users_repository.add(user)

        self.change_current(user)

    def sign_out(self, user: User) -> None:
        if not self.is_authorized(user):
            return

        try:
            if user.id == json.load(open(CURENT_USER_FILE_PATH))["id"]:
                try:
                    with open(CURENT_USER_FILE_PATH, "w") as file:
                        pass
                except:
                    pass
        except:
            pass
        
        self._auth_users_repository.delete(user)
        self._not_auth_users_repository.add(user)
    
    def is_authorized(self, user: User) -> bool:
        return self._auth_users_repository.get_by_id(user.id) != None

    def current_user(self, user: User) -> None:
        self.change_current(user)
    
    def change_current(self, user: User) -> None:
        try:
            with open(CURENT_USER_FILE_PATH, "w") as file:
                json.dump({"id": user.id, "login": user.login}, file, indent=4)
        except:
            pass
    
    def sign_up(self, user: User) -> None:
        if self._auth_users_repository.get_by_id(user.id) != None or self._not_auth_users_repository.get_by_id(user.id) != None:
            return

        self._auth_users_repository.add(user)
