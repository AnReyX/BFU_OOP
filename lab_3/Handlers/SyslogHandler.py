from LogLevel import LogLevel
from Handlers.ILogHandler import ILogHandler

class SyslogHandler(ILogHandler):
    def __init__(self, log_file: str) -> None:
        self.log_file = log_file

    def handle(self, log_level: LogLevel, text: str) -> None:
        try:
            with open(self.log_file, "a") as file:
                file.write(text + '\n')
        except:
            return