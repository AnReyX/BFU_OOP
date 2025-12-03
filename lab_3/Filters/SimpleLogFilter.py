from Filters.ILogFilter import ILogFilter
from LogLevel import LogLevel

class SimpleLogFilter(ILogFilter):
    def __init__(self, filter_str: str) -> None:
        self.filter_str = filter_str

    def match(self, log_level: LogLevel, text: str) -> bool:
        return self.filter_str in text
        