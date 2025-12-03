from enum import Enum

class AnsiColor(Enum):
    # Стандартные цвета ANSI
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"  # Сброс цвета


class AnsiCommand:
    # Команды управления курсором
    SAVE_CURSOR = "\033[s"  # Сохранить позицию курсора
    RESTORE_CURSOR = "\033[u"  # Восстановить позицию
    CLEAR_SCREEN = "\033[2J"  # Очистить экран

    @staticmethod
    def move_cursor(x: int, y: int) -> str:
        return f"\033[{y};{x}H"