import json
import sys
from enum import Enum
from typing import Tuple, List


# ---------------------------------------------------------
# 1. КОНСТАНТЫ И ENUM (Управляющие команды)
# ---------------------------------------------------------

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
        """Генерирует команду перемещения курсора в (y, x). В ANSI это row;col"""
        return f"\033[{y};{x}H"


# ---------------------------------------------------------
# 2. КЛАСС PRINTER
# ---------------------------------------------------------

class Printer:
    def __init__(self, color: AnsiColor, position: Tuple[int, int], symbol: str, font_path: str):
        """
        Конструктор для использования в блоке with.
        """
        self.color = color
        self.position = position  # (x, y)
        self.symbol = symbol
        self.font_path = font_path
        self.font_data = self._load_font(font_path)
        self._current_offset_y = 0  # Чтобы следующий print внутри with не накладывался

    # --- Вспомогательные методы (скрытые) ---

    @staticmethod
    def _load_font(path: str) -> dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Ошибка: Файл шрифта {path} не найден.")
            sys.exit(1)

    @staticmethod
    def _generate_art_lines(text: str, font_data: dict, symbol: str) -> List[str]:
        """
        Превращает текст 'HI' в список строк псевдографики.
        """
        char_height = font_data.get('height', 5)
        chars_dict = font_data.get('chars', {})

        # Получаем шаблоны для каждой буквы. Если буквы нет, берем '?' (или пробел)
        # chars_dict.get(char, [...]) возвращает список строк для буквы
        matrix = []
        for char in text.upper():
            if char in chars_dict:
                matrix.append(chars_dict[char])
            else:
                # Заглушка для неизвестных символов (просто пробелы)
                matrix.append([" " * 5] * char_height)

        # Самая магия Python: склеиваем буквы горизонтально
        # zip(*matrix) берет первую строку у всех букв, потом вторую...
        lines = []
        for rows in zip(*matrix):
            # Соединяем строки букв с небольшим отступом
            joined_line = "  ".join(rows)
            # Заменяем шаблонный '*' на пользовательский символ
            lines.append(joined_line.replace('*', symbol))

        return lines

    # --- Основной функционал ---

    @classmethod
    def print_static(cls, text: str, color: AnsiColor, position: Tuple[int, int], symbol: str, font_path: str):
        """
        Статический метод для разового вывода.
        """
        # 1. Загружаем шрифт
        font_data = cls._load_font(font_path)

        # 2. Генерируем строки
        art_lines = cls._generate_art_lines(text, font_data, symbol)

        # 3. Выводим
        x, y = position
        print(AnsiCommand.SAVE_CURSOR, end='')  # Сохраняем, где были до этого

        for i, line in enumerate(art_lines):
            cursor_cmd = AnsiCommand.move_cursor(x, y + i)
            # Вывод: Позиция -> Цвет -> Текст -> Сброс цвета
            print(f"{cursor_cmd}{color.value}{line}{AnsiColor.RESET.value}", end='', flush=True)

        print(AnsiCommand.RESTORE_CURSOR, end='')  # Возвращаем курсор (опционально)

    def print(self, text: str):
        """
        Метод экземпляра. Использует сохраненные настройки.
        Сдвигает позицию вниз для следующего вызова, чтобы текст не накладывался.
        """
        art_lines = self._generate_art_lines(text, self.font_data, self.symbol)

        x, y = self.position
        # Смещаем Y на накопленный отступ (если вызываем print несколько раз внутри with)
        start_y = y + self._current_offset_y

        for i, line in enumerate(art_lines):
            cursor_cmd = AnsiCommand.move_cursor(x, start_y + i)
            print(f"{cursor_cmd}{self.color.value}{line}", end='', flush=True)  # Цвет не сбрасываем тут, сбросим в exit

        # Обновляем отступ для следующего вызова (высота текста + 1 строка отступа)
        self._current_offset_y += len(art_lines) + 1

    # --- Context Manager (with) ---

    def __enter__(self):
        # При входе сохраняем состояние курсора
        print(AnsiCommand.SAVE_CURSOR, end='')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # При выходе сбрасываем цвет и возвращаем курсор
        print(AnsiColor.RESET.value, end='')
        print(AnsiCommand.RESTORE_CURSOR, end='')
        # Нужно переместить курсор в самый низ, чтобы консоль не перезаписала графику,
        # если программа завершится сразу. Но по заданию "возврат в исходное".
        # Оставим RESTORE_CURSOR как наиболее строгое выполнение условия.


# ---------------------------------------------------------
# 3. ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ (ШРИФТЫ)
# ---------------------------------------------------------

def create_font_files():
    """Создает json файлы со шрифтами для демонстрации"""

    # Шрифт 5 символов высотой
    font5 = {
        "height": 5,
        "chars": {
            "H": ["*   *", "*   *", "*****", "*   *", "*   *"],
            "E": ["*****", "*    ", "*****", "*    ", "*****"],
            "L": ["*    ", "*    ", "*    ", "*    ", "*****"],
            "O": [" *** ", "*   *", "*   *", "*   *", " *** "],
            "1": ["  *  ", " **  ", "  *  ", "  *  ", "*****"]
        }
    }

    # Шрифт 7 символов высотой (более тонкий)
    font7 = {
        "height": 7,
        "chars": {
            "W": ["*     *", "*     *", "*     *", "*  *  *", "* * * *", "**   **", "*     *"],
            "O": ["  ***  ", " *   * ", "*     *", "*     *", "*     *", " *   * ", "  ***  "],
            "R": ["****** ", "*     *", "*     *", "****** ", "*   *  ", "*    * ", "*     *"],
            "L": ["*      ", "*      ", "*      ", "*      ", "*      ", "*      ", "*******"],
            "D": ["****** ", "*     *", "*     *", "*     *", "*     *", "*     *", "****** "],
            "2": [" ***** ", "*     *", "      *", "     * ", "   **  ", " **    ", "*******"]
        }
    }

    with open("font5.json", "w") as f:
        json.dump(font5, f)
    with open("font7.json", "w") as f:
        json.dump(font7, f)


# ---------------------------------------------------------
# 4. ДЕМОНСТРАЦИЯ (MAIN)
# ---------------------------------------------------------

if __name__ == "__main__":
    # Сначала создадим файлы шрифтов
    create_font_files()

    # Очистим экран для красоты
    print(AnsiCommand.CLEAR_SCREEN, end='')

    # ДЕМО 1: Статический вызов (Static Method)
    # Выводим "HELLO" красным цветом, символом '#', в позиции (100, 10)
    # Используем шрифт font5.json
    Printer.print_static(
        text="HELLO",
        color=AnsiColor.RED,
        position=(100, 10),
        symbol="#",
        font_path="font5.json"
    )

    # ДЕМО 2: Использование экземпляра и with (Context Manager)
    # Выводим текст синим цветом, символом '@', начиная с позиции (10, 5)
    # Используем шрифт font7.json

    with Printer(AnsiColor.BLUE, (10, 5), "@", "font7.json") as printer:
        printer.print("WORLD")
        # Следующий текст выведется ниже предыдущего автоматически
        printer.print("WRD2")

        # Переместим курсор вниз, чтобы системные сообщения не затерли рисунок
    print(AnsiCommand.move_cursor(1, 25))
    print("Работа завершена.")
