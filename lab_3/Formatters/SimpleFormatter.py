from LogLevel import LogLevel
from Formatters.ILogFormatter import ILogFormatter
import time

class SimpleFormatter(ILogFormatter):
    def format(self, log_level: LogLevel, text: str) -> str:
        time_gm = time.gmtime()
        time_str = f'{time_gm.tm_year}.{time_gm.tm_mon}.{time_gm.tm_mday} {time_gm.tm_hour}:{time_gm.tm_min}:{time_gm.tm_sec}'
        return f'[{log_level.name}] [{time_str}] {text}'
