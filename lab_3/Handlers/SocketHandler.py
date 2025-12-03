from LogLevel import LogLevel
from Handlers.ILogHandler import ILogHandler

class SocketHandler(ILogHandler):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def handle(self, log_level: LogLevel, text: str) -> None:
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.host, self.port))
            
            s.sendall(text.encode('utf-8'))

            s.close()
        except:
            return