from LogLevel import LogLevel

class ILogHandler:
    def handle(self, log_level: LogLevel, text: str) -> None:
        ...