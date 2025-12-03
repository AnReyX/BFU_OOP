from LogLevel import LogLevel
from Handlers.ILogHandler import ILogHandler
import os

class FileHandler(ILogHandler):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def handle(self, log_level: LogLevel, text: str) -> None:
        if not os.path.exists(self.file_path):
            return
        
        try:
            with open(self.file_path, "a") as file:
                file.write(text + '\n')
        except:
            return