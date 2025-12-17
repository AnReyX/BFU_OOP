from IAuthService import IAuthService
from UserRepository import UserRepository
from User import User
from typing import Optional
import json
import os

class AuthService(IAuthService):
    def __init__(self, user_repo: UserRepository, session_file: str = "session.json"):
        self._user_repo = user_repo
        self._session_file = session_file
        self._current_user: Optional[User] = None

        self._try_auto_auth()

    def _try_auto_auth(self) -> None:
        if os.path.exists(self._session_file):
            try:
                with open(self._session_file, encoding='utf-8') as f:
                    data = json.load(f)
                    user_id = data.get("user_id")
                    if user_id is not None:
                        user = self._user_repo.get_by_id(user_id)
                        if user:
                            print(f"[Auth] Авто-вход выполнен: {user.login}")
                            self._current_user = user
            except Exception:
                pass

    def sign_in(self, login: str, password: str) -> None:
        user = self._user_repo.get_by_login(login)
        if user and user.password == password:
            self._current_user = user
            with open(self._session_file, 'w', encoding='utf-8') as f:
                json.dump({"user_id": user.id}, f)

    def sign_out(self) -> None:
        self._current_user = None
        if os.path.exists(self._session_file):
            os.remove(self._session_file)

    def is_authorized(self) -> bool:
        return self._current_user is not None

    def current_user(self) -> Optional[User]:
        return self._current_user