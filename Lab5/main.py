from User import User
from UserRepository import UserRepository
from AuthService import AuthService

def main():
    db_file = "users.json"
    session_file = "session.json"

    user_repo = UserRepository(db_file)
    auth_service = AuthService(user_repo, session_file)

    if auth_service.is_authorized():
        print(f"Добро пожаловать обратно, {auth_service.current_user().name}")
    else:
        print("Вы не авторизованы.")

    if not user_repo.get_all():
        print("\n- - - Инициализация бд - - -")
        u1 = User(id=1, name="Андрей Голубин", login="andrew", password="123", email="andrew@mail.ru")
        u2 = User(id=2, name="Владислав Целиковский", login="vlad", password="321")
        u3 = User(id=3, name="Виктор Антонников", login="victor", password="qwerty")

        user_repo.add(u1)
        user_repo.add(u2)
        user_repo.add(u3)
        print("Добавили пользователей в users.json")

    print("\n- - - Сортировка по имени - - -")
    users = list(user_repo.get_all())
    users.sort()
    for u in users:
        print(u)

    if not auth_service.is_authorized:
        print("\n- - - Вход в систему - - -")
        auth_service.sign_in("anna", "321")
        if auth_service.is_authorized():
            print(f"Успешный вход: {auth_service.current_user()}")
        else:
            print("Неверный логин / пароль")

    if auth_service.is_authorized():
        print("\n- - - Обновление данных пользователя - - -")
        me = auth_service.current_user()
        me.address = "г. Москва, ул. Пушкина, д. 10"
        user_repo.update(me)
        print("Адрес текущего пользователя в users обновлен.")

    print("\n- - - Смена пользователя - - -")
    auth_service.sign_out()
    print("Вышли из системы.")

    auth_service.sign_in("andrew", "123")
    if auth_service.is_authorized():
        print(f"Теперь вошел: {auth_service.current_user().name}")


if __name__ == "__main__":
    main()