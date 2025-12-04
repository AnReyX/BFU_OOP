from abc import ABC, abstractmethod
import re
import socket
import datetime
from enum import IntEnum
from typing import List


# ==========================================
# 1. Перечислитель LogLevel
# Используем IntEnum, чтобы можно было сравнивать уровни (ERROR > INFO)
# ==========================================
class LogLevel(IntEnum):
    INFO = 1
    WARN = 2
    ERROR = 3


# ==========================================
# 2. Абстракция (Интерфейс) Фильтра
# ==========================================
class ILogFilter(ABC):
    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool:
        """Возвращает True, если лог должен пройти, иначе False"""
        pass


# ==========================================
# 3. Реализация Фильтров
# ==========================================
class SimpleLogFilter(ILogFilter):
    """Пропускает лог, если в тексте содержится заданная подстрока"""

    def __init__(self, keyword: str):
        self.keyword = keyword

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.keyword in text


class ReLogFilter(ILogFilter):
    """Пропускает лог, если текст соответствует регулярному выражению"""

    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.pattern.search(text) is not None


class LevelFilter(ILogFilter):
    """
    Пропускает лог, если его уровень равен заданному
    """

    def __init__(self, level: LogLevel):
        self.level = level

    def match(self, log_level: LogLevel, text: str) -> bool:
        return log_level == self.level


# ==========================================
# 4. Абстракция (Интерфейс) Обработчика (Handler)
# ==========================================
class ILogHandler(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        pass


# ==========================================
# 5. Реализация Обработчиков
# ==========================================
class ConsoleHandler(ILogHandler):
    def handle(self, log_level: LogLevel, text: str) -> None:
        # Вывод в стандартный поток вывода (консоль)
        print(f"[CONSOLE] {text}")


class FileHandler(ILogHandler):
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        # 'a' - append mode (добавление в конец файла)
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(f"{text}\n")


class SocketHandler(ILogHandler):
    """Имитация отправки в сокет (чтобы код не падал без реального сервера)"""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            '''
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))

            s.sendall(text.encode('utf-8'))

            s.close()'''
            print(f"[SOCKET -> {self.host}:{self.port}] {text}")
        except Exception as e:
            print(f"Socket Error: {e}")


class SyslogHandler(ILogHandler):
    """Имитация записи в системный лог"""

    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[SYSLOG] {text}")


class FtpHandler(ILogHandler):
    """Имитация отправки на FTP"""

    def __init__(self, ftp_host: str):
        self.ftp_host = ftp_host

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            '''
                with open(self.message_file, "w") as file:
                    file.write(text)
    
                with open(self.message_file, 'rb') as file:
                    ftp = FTP(self.server)
    
                    ftp.login(self.usernamer, self.password)
                    ftp.storbinary(f"STOR {self.message_file}", file)
    
                    ftp.quit()
            '''
            print(f"[FTP -> {self.ftp_host}] Uploading log: {text}")
        except Exception as e:
            print(f"FTP Error: {e}")


# ==========================================
# 6. Абстракция (Интерфейс) Форматтера
# ==========================================
class ILogFormatter(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        pass


# ==========================================
# 7. Реализация Форматтера
# ==========================================
class StandardFormatter(ILogFormatter):
    """
    Форматирует сообщение к виду:
    [<log_level>] [<data:yyyy.MM.dd hh:mm:ss>] <text>
    """

    def format(self, log_level: LogLevel, text: str) -> str:
        # Получаем имя уровня (например, "INFO")
        level_name = log_level.name
        # Текущее время
        now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")

        return f"[{level_name}] [{now}] {text}"


# ==========================================
# 8. Класс Logger (Композиция)
# ==========================================
class Logger:
    def __init__(
            self,
            filters: List[ILogFilter] = None,
            formatters: List[ILogFormatter] = None,
            handlers: List[ILogHandler] = None
    ):
        # Если списки не переданы, инициализируем пустыми
        self.filters = filters if filters else []
        self.formatters = formatters if formatters else []
        self.handlers = handlers if handlers else []

    def log(self, log_level: LogLevel, text: str) -> None:
        # 1. Проверка фильтров
        # Если хотя бы один фильтр вернет False, лог не проходит
        for log_filter in self.filters:
            if not log_filter.match(log_level, text):
                return  # Прерываем обработку, лог отфильтрован

        # 2. Применение форматтеров (последовательно)
        formatted_text = text
        for formatter in self.formatters:
            formatted_text = formatter.format(log_level, formatted_text)

        # 3. Отправка обработчикам
        for handler in self.handlers:
            handler.handle(log_level, formatted_text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)


# ==========================================
# 9. Демонстрация работы
# ==========================================
if __name__ == "__main__":
    print("=== Настройка системы логирования ===\n")

    # Создаем компоненты

    # Фильтры:
    # 1. Пропускать только если уровень >= WARN
    level_filter = LevelFilter(LogLevel.WARN)
    # 2. Пропускать только если в тексте нет слова "secret" (для примера инвертируем логику внутри фильтра сложно,
    # поэтому используем позитивные фильтры из задания.
    # Допустим, мы хотим логировать только сообщения, содержащие слово "System" (SimpleFilter)
    # или сообщения, начинающиеся с кода ошибки Error-XXX (RegexFilter).
    # Для простоты демонстрации добавим только LevelFilter, иначе слишком много логов отсеется.

    # Форматтеры:
    std_formatter = StandardFormatter()

    # Обработчики:
    console_handler = ConsoleHandler()
    file_handler = FileHandler("app_logs.txt")
    # Чтобы не засорять вывод ошибками сети, используем mock-реализации внутри классов
    socket_handler = SocketHandler("127.0.0.1", 8080)

    # --- Сценарий 1: Строгий логгер (только ошибки в файл и консоль) ---
    print("--- Logger 1: Strict (Errors Only) ---")
    strict_logger = Logger(
        filters=[LevelFilter(LogLevel.ERROR)],
        formatters=[std_formatter],
        handlers=[console_handler, file_handler]
    )

    strict_logger.log_info("Это сообщение INFO не должно появиться.")
    strict_logger.log_warn("Это сообщение WARN тоже не появится.")
    strict_logger.log_error("Критическая ошибка базы данных!")  # Это должно появиться

    print("\n--- Logger 2: General (Info+, Regex filter) ---")
    # --- Сценарий 2: Логгер для определенных сообщений ---
    # Пропускаем всё, что INFO и выше, НО текст должен содержать цифры (Regex)
    regex_filter = ReLogFilter(r"\d+")  # Паттерн: наличие хотя бы одной цифры

    general_logger = Logger(
        filters=[LevelFilter(LogLevel.INFO), regex_filter],
        formatters=[std_formatter],
        handlers=[console_handler, socket_handler]
    )

    general_logger.log_info("Запуск системы...")  # Нет цифр -> отфильтруется
    general_logger.log_info("Запуск сервиса 1")  # Есть цифра -> пройдет
    general_logger.log_warn("Память заполнена на 90%")  # Есть цифры -> пройдет

    print("\n--- Проверка файла app_logs.txt ---")
    try:
        with open("app_logs.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:

        print("Файл логов еще не создан.")
