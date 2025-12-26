from typing import Callable, Any, Optional
from enum import Enum
import inspect
from abc import ABC, abstractmethod


class LifeStyle(Enum):
    PerRequest = "PerRequest"
    Scoped = "Scoped"
    Singleton = "Singleton"


class Injector:
    def __init__(self) -> None:
        self.registrations = {}
        self.singletons = {}
        self.scopes = []

    def register(self, interface: object, cls_func: object | Callable, 
                 lifestyle: Optional[LifeStyle] = None, 
                 parameters: Optional[dict[str, Any]] = None) -> None:
        if inspect.isclass(cls_func):
            sig = inspect.signature(cls_func.__init__)
            for name, parameter in sig.parameters.items():
                if name == "self":
                    continue
                if parameter.annotation != inspect.Parameter.empty and parameter.annotation not in self.registrations:
                    raise Exception(f"You should registrate '{parameter.annotation}'")
        self.registrations[interface] = {
            'target': cls_func,
            'lifestyle': lifestyle,
            'parameters': parameters if parameters else {}
        }

    def get_instance(self, interface: type) -> Any:
        if interface not in self.registrations:
            raise KeyError(f"Interface '{interface}' not registered")
        
        reg = self.registrations[interface]
        target = reg["target"]
        parameters = reg["parameters"]
        lifestyle = reg["lifestyle"]

        if lifestyle == LifeStyle.Singleton and interface in self.singletons:
            return self.singletons[interface]
        
        if lifestyle == LifeStyle.Scoped and self.scopes and interface in self.scopes[-1]:
            return self.scopes[-1][interface]

        if inspect.isclass(target):
            sign = inspect.signature(target.__init__)
            args = {}

            for name, parameter in sign.parameters.items():
                if name in ["self", "args", "kwargs"]:
                    continue
                if name in parameters:
                    args[name] = parameters[name]
                elif parameter.annotation != inspect.Parameter.empty and parameter.annotation in self.registrations:
                    args[name] = self.get_instance(parameter.annotation)
                elif parameter.default != inspect.Parameter.empty:
                    args[name] = parameter.default
                else:
                    raise Exception(f"Cannot resolve parameter '{name}'")

            obj = target(**args)
        else:
            obj = target(**parameters)

        if lifestyle == LifeStyle.Singleton:
            self.singletons[interface] = obj
        elif lifestyle == LifeStyle.Scoped:
            if not self.scopes:
                raise Exception("No active scope")
            self.scopes[-1][interface] = obj
        return obj
    
    def open_scope(self) -> object:
        return Scope(self)
    

class Scope:
    def __init__(self, injector: Injector) -> None:
        self.injector = injector

    def __enter__(self) -> Injector:
        self.injector.scopes.append({})
        return self.injector
    
    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.injector.scopes.pop()

from abc import ABC, abstractmethod
import random

# --- Импортируем твой код (или вставь класс Injector сюда) ---
# from my_injector import Injector, LifeStyle 
# (Для удобства я предполагаю, что класс Injector и LifeStyle уже здесь или импортированы)

# ==========================================
# 2. ОПРЕДЕЛЕНИЕ ИНТЕРФЕЙСОВ И КЛАССОВ
# ==========================================

# Интерфейс 1: Логгер
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str): pass

# Реализация 1.1 (Debug)
class ConsoleLogger(ILogger):
    def __init__(self):
        self.id = random.randint(1, 1000)
        print(f"[ConsoleLogger Created] ID: {self.id}")

    def log(self, message: str):
        print(f"LOG (ID {self.id}): {message}")

# Реализация 1.2 (Release)
class FileLogger(ILogger):
    def __init__(self, path: str = "default.log"):
        self.path = path
        self.id = random.randint(1, 1000)
        print(f"[FileLogger Created] ID: {self.id}, Path: {self.path}")

    def log(self, message: str):
        print(f"WRITING TO FILE {self.path} (ID {self.id}): {message}")

# ---

# Интерфейс 2: База данных
class IDatabase(ABC):
    @abstractmethod
    def connect(self): pass

# Реализация 2.1 (Debug) - InMemory
class InMemoryDatabase(IDatabase):
    def connect(self):
        return "Connected to Memory"

# Реализация 2.2 (Release) - Postgres
class PostgresDatabase(IDatabase):
    def connect(self):
        return "Connected to Postgres"

# ---

# Интерфейс 3: Сервис уведомлений (Фабричный метод будет тут)
class INotification(ABC):
    @abstractmethod
    def send(self, msg): pass

class EmailNotification(INotification):
    def send(self, msg): print(f"Email sent: {msg}")

# Фабричный метод
def notification_factory(prefix: str = ""):
    print(f"Factory called with prefix: {prefix}")
    inst = EmailNotification()
    # Можем как-то настроить объект
    return inst

# ---

# Сложный класс, использующий зависимости (Внедрение зависимостей)
class UserService:
    # Инжектор посмотрит на аннотации типов ILogger и IDatabase
    def __init__(self, logger: ILogger, db: IDatabase):
        self.logger = logger
        self.db = db
    
    def register_user(self, name: str):
        self.logger.log(f"Registering user {name}")
        conn = self.db.connect()
        self.logger.log(f"DB Status: {conn}")

# ==========================================
# 3. КОНФИГУРАЦИИ (DEBUG / RELEASE)
# ==========================================

def configure_debug(container: Injector):
    print("\n--- Applying DEBUG Config ---")
    # Сначала регистрируем зависимости (листья), потом зависимые сервисы!
    
    # Singleton: Логгер один на всё приложение
    container.register(ILogger, ConsoleLogger, LifeStyle.Singleton)
    
    # Scoped: База данных (одна на запрос/область)
    container.register(IDatabase, InMemoryDatabase, LifeStyle.Scoped)
    
    # PerRequest: Сервис создается каждый раз новый
    container.register(UserService, UserService, LifeStyle.PerRequest)

def configure_release(container: Injector):
    print("\n--- Applying RELEASE Config ---")
    
    # Передаем параметры в конструктор (путь к файлу)
    container.register(ILogger, FileLogger, LifeStyle.Singleton, parameters={"path": "/var/log/app.log"})
    
    container.register(IDatabase, PostgresDatabase, LifeStyle.Singleton)
    
    # Фабричный метод
    container.register(INotification, notification_factory, parameters={"prefix": "ALERT"})
    
    container.register(UserService, UserService, LifeStyle.PerRequest)

# ==========================================
# 4. ДЕМОНСТРАЦИЯ И ТЕСТЫ
# ==========================================

def run_tests():
    injector = Injector()
    
    # --- СЦЕНАРИЙ 1: DEBUG (Singleton + Scoped + Auto Injection) ---
    configure_debug(injector)
    
    print("\n1. Проверка Singleton (Logger):")
    log1 = injector.get_instance(ILogger)
    log2 = injector.get_instance(ILogger)
    print(f"Log1 ID: {log1.id}, Log2 ID: {log2.id}")
    assert log1 is log2, "Singleton должен возвращать один и тот же объект"
    print("SUCCESS: Logger is Singleton")

    print("\n2. Проверка Scoped (Database):")
    # Попытка получить Scoped без scope должна вызвать ошибку (или вернуть, если логика позволяет, но у тебя проверка if not self.scopes)
    try:
        injector.get_instance(IDatabase)
    except Exception as e:
        print(f"Ожидаемая ошибка без scope: {e}")

    with injector.open_scope():
        db1 = injector.get_instance(IDatabase)
        db2 = injector.get_instance(IDatabase)
        assert db1 is db2, "Внутри одного Scope объекты должны быть одинаковы"
        print(f"Inside Scope 1: DBs are same object. Connection: {db1.connect()}")
    
    with injector.open_scope():
        db3 = injector.get_instance(IDatabase)
        assert db1 is not db3, "В разных Scope объекты должны быть разными"
        print("Inside Scope 2: DB is a new object.")
    print("SUCCESS: Scoped works correctly")

    print("\n3. Проверка автоматического внедрения (UserService):")
    # UserService требует ILogger и IDatabase. Инжектор сам их найдет.
    # Так как IDatabase у нас Scoped, нам нужен активный scope для создания UserService
    with injector.open_scope():
        user_service = injector.get_instance(UserService)
        user_service.register_user("Ivan")
        # Проверяем, что внутри сервиса лежат правильные типы
        assert isinstance(user_service.logger, ConsoleLogger)
        assert isinstance(user_service.db, InMemoryDatabase)
    print("SUCCESS: Dependencies injected automatically")

    # --- СЦЕНАРИЙ 2: RELEASE (Factory + Params) ---
    # Создаем новый инжектор для чистоты эксперимента
    injector_rel = Injector()
    configure_release(injector_rel)

    print("\n4. Проверка параметров (FileLogger path):")
    f_log = injector_rel.get_instance(ILogger)
    assert f_log.path == "/var/log/app.log"
    print(f"SUCCESS: Parameter injected. Path is {f_log.path}")

    print("\n5. Проверка фабричного метода:")
    # Фабрика возвращает EmailNotification
    notify = injector_rel.get_instance(INotification)
    notify.send("Hello World") 
    assert isinstance(notify, EmailNotification)
    print("SUCCESS: Factory method worked")

if __name__ == "__main__":
    run_tests()
