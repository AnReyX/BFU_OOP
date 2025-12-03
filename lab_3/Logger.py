from Filters.ILogFilter import ILogFilter
from Formatters.ILogFormatter import ILogFormatter
from Handlers.ILogHandler import ILogHandler
from LogLevel import LogLevel

class Logger:
    def __init__(self, filters: list[ILogFilter], formaters: list[ILogFormatter], handlers: list[ILogHandler]) -> None:
        self.filters = filters
        self.formaters = formaters
        self.handlers = handlers
    
    def log(self, log_level: LogLevel, text: str) -> None:
        for filtrator in self.filters:
            if not filtrator.match(log_level, text):
                return
        
        for formater in self.formaters:
            text = formater.format(log_level, text)
        
        for handler in self.handlers:
            handler.handle(log_level, text)
    
    def log_info(self, text: str) -> None:
        self.log(LogLevel.INFO, text)
    
    def log_warn(self, text: str) -> None:
        self.log(LogLevel.WARN, text)
    
    def log_error(self, text: str) -> None:
        self.log(LogLevel.ERROR, text)