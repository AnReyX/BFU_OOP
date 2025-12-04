from abc import ABC, abstractmethod
import re
import socket
import datetime
from enum import Enum
from typing import List


#Перечислитель LogLevel
class LogLevel(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3


# Интерфейс фильтра
class ILogFilter(ABC):
    @abstractmethod
    def match(self, log_level: LogLevel, text: str) -> bool:
        pass


# Фильтры
class SimpleLogFilter(ILogFilter): # Пропуск, если содержит ключевое слово

    def __init__(self, keyword: str):
        self.keyword = keyword.lower()

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.keyword in text.lower()


class ReLogFilter(ILogFilter): # Пропуск, если текст соответствует регулярному выражению

    def __init__(self, pattern: str):
        try:
            self.pattern = re.compile(pattern)
        except Exception as e:
            print(f"RegEx Error: {e}")

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.pattern.search(text) is not None


class LevelFilter(ILogFilter): # Пропуск, если его уровень равен заданному

    def __init__(self, level: LogLevel):
        self.level = level

    def match(self, log_level: LogLevel, text: str) -> bool:
        return log_level == self.level


# Интерфейс обработчика (Handler)
class ILogHandler(ABC):
    @abstractmethod
    def handle(self, log_level: LogLevel, text: str) -> None:
        pass


# Обработчики
class ConsoleHandler(ILogHandler): # Вывод в стандартный поток вывода (консоль)

    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[CONSOLE] {text}")


class FileHandler(ILogHandler): # Вывод в текстовый файл

    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            # 'a' - append mode (добавление в конец файла)
            with open(self.filename, "a", encoding="utf-8") as f:
                f.write(f"{text}\n")
        except Exception as e:
            print(f"File Handler Error: {e}")


class SocketHandler(ILogHandler): # Отправка в сокет

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


class SyslogHandler(ILogHandler): # Запись в системный лог

    def handle(self, log_level: LogLevel, text: str) -> None:
        print(f"[SYSLOG] {text}")


class FtpHandler(ILogHandler): # Отправка на FTP

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


# Интерфейс форматтера
class ILogFormatter(ABC):
    @abstractmethod
    def format(self, log_level: LogLevel, text: str) -> str:
        pass


# Форматтер
class StandardFormatter(ILogFormatter):
    """
    Форматирует сообщение к виду:
    [<log_level>] [<data:yyyy.MM.dd hh:mm:ss>] <text>
    """

    def format(self, log_level: LogLevel, text: str, date_format: str = "%Y.%m.%d %H:%M:%S") -> str:
        try:
            level_name = log_level.name
            now = datetime.datetime.now().strftime(date_format)

            return f"[{level_name}] [{now}] {text}"
        except Exception as e:
            print(f"Formatting Error: {e}")


# Класс Logger, композиция
class Logger:
    def __init__(self, filters: List[ILogFilter] = None, formatters: List[ILogFormatter] = None, handlers: List[ILogHandler] = None):
        # Если списки не переданы, инициализируем пустыми
        self.filters = filters if filters else []
        self.formatters = formatters if formatters else []
        self.handlers = handlers if handlers else []

    def log(self, log_level: LogLevel, text: str) -> None:
        for log_filter in self.filters:
            if not log_filter.match(log_level, text): # Если хотя бы один фильтр вернет False, лог не проходит
                return

        formatted_text = text
        for formatter in self.formatters: # Форматирование
            formatted_text = formatter.format(log_level, formatted_text)

        for handler in self.handlers: # Отправка обработчикам
            handler.handle(log_level, formatted_text)

    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)

    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)

    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)



if __name__ == "__main__":

    # Фильтры
    level_filter_E = LevelFilter(LogLevel.ERROR) # Фильтры: Пропускать только если уровень == ERROR
    level_filter_I = LevelFilter(LogLevel.INFO) # Пропускать только если уровень == INFO

    std_formatter = StandardFormatter() # Форматтер

    # Обработчики:
    console_handler = ConsoleHandler()
    file_handler = FileHandler("app_logs.txt")
    socket_handler = SocketHandler("127.0.0.1", 8080)

    print("- - - Logger 1: Strict (Errors Only) - - -")
    strict_logger = Logger(filters=[LevelFilter(LogLevel.ERROR)], formatters=[std_formatter], handlers=[console_handler, file_handler])

    strict_logger.log_info("Это сообщение INFO не должно появиться.")
    strict_logger.log_warn("Это сообщение WARN тоже не появится.")
    strict_logger.log_error("Критическая ошибка базы данных!")  # Это должно появиться

    print("\n- - - Logger 2: General (Info+, Regex filter) - - -")
    regex_filter = ReLogFilter(r"\d+")  # Паттерн: наличие хотя бы одной цифры

    general_logger = Logger(filters=[LevelFilter(LogLevel.INFO), regex_filter], formatters=[std_formatter], handlers=[console_handler, socket_handler])

    general_logger.log_info("Запуск системы...")  # Нет цифр -> отфильтруется
    general_logger.log_info("Запуск сервиса 1")  # Есть цифра -> пройдет
    general_logger.log_warn("Память заполнена на 90%")  # Есть цифры -> пройдет

    print("\n- - - Проверка файла app_logs.txt - - -")
    try:
        with open("app_logs.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Файл логов еще не создан.")
