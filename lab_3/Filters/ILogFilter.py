from LogLevel import LogLevel

class ILogFilter:
    def match(self, log_level: LogLevel, text: str) -> bool:
        ...