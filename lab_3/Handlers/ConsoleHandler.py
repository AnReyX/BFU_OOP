from LogLevel import LogLevel
from Handlers.ILogHandler import ILogHandler

class ConsoleHandler(ILogHandler):

    def handle(self, log_level: LogLevel, text: str) -> None:
        print(text)