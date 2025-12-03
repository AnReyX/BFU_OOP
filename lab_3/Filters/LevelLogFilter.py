from Filters.ILogFilter import ILogFilter
from LogLevel import LogLevel

class LevelLogFilter(ILogFilter):
    def __init__(self, level: LogLevel) -> None:
        self.level = level

    def match(self, log_level: LogLevel, text: str) -> bool:
        return log_level.value == self.level.value