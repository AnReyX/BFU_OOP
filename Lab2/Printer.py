import sys
import json
from typing import Tuple, List
from ANSI import AnsiColor, AnsiCommand

class Printer:
    def __init__(self, color: AnsiColor, position: Tuple[int, int], symbol: str, font_path: str):
        self.color = color
        self.position = position  # (x, y)
        self.symbol = symbol
        self.font_path = font_path
        self.font_data = self._load_font(font_path)
        self._current_offset_y = 0  # Чтобы следующий print внутри with не накладывался

    # - - - Вспомогательные статические методы - - -

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
        char_height = font_data.get('height', 5)
        chars_dict = font_data.get('chars', {})

        # Получаем шаблоны для каждой буквы. Если буквы нет, берем '?' (или пробел)
        # chars_dict.get(char, [...]) возвращает список строк для буквы
        matrix = []
        for char in text.upper():
            if char in chars_dict:
                matrix.append(chars_dict[char])
            else:
                # Заглушка для неизвестных символов, пробелы
                matrix.append([" " * 5] * char_height)

        # Склеиваем буквы горизонтально: zip(*matrix) берет первую строку у всех букв, вторую и тд
        lines = []
        for rows in zip(*matrix):
            joined_line = "  ".join(rows) # Соединяем строки букв с небольшим отступом
            lines.append(joined_line.replace('*', symbol)) # Заменяем шаблонный '*' на пользовательский символ

        return lines

    # - - - Основной функционал - - -

    @classmethod
    def print_static(cls, text: str, color: AnsiColor, position: Tuple[int, int], symbol: str, font_path: str) -> None:
        font_data = cls._load_font(font_path) # Загружаем шрифт

        art_lines = cls._generate_art_lines(text, font_data, symbol) # Генерируем строки

        x, y = position # Выводим
        print(AnsiCommand.SAVE_CURSOR, end='')  # Сохраняем, где были до этого

        for i, line in enumerate(art_lines):
            cmd = AnsiCommand.move_cursor(x, y + i)
            # Вывод: Позиция -> Цвет -> Текст -> Сброс цвета
            print(f"{cmd}{color.value}{line}{AnsiColor.RESET.value}", end='', flush=True)

        print(AnsiCommand.RESTORE_CURSOR, end='')  # Возвращаем курсор (опционально)

    def print(self, text: str) -> None:
        art_lines = self._generate_art_lines(text, self.font_data, self.symbol)

        x, y = self.position
        # Смещаем Y на накопленный отступ (если вызываем print несколько раз внутри with)
        start_y = y + self._current_offset_y

        for i, line in enumerate(art_lines):
            cursor_cmd = AnsiCommand.move_cursor(x, start_y + i)
            print(f"{cursor_cmd}{self.color.value}{line}", end='', flush=True)  # Цвет не сбрасываем тут, сбросим в exit

        # Обновляем отступ для следующего вызова (высота текста + 1 строка отступа)
        self._current_offset_y += len(art_lines) + 1

    # - - - Context Manager (with) - - -

    def __enter__(self):
        print(AnsiCommand.SAVE_CURSOR, end='') # При входе сохраняем состояние курсора
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # При выходе сбрасываем цвет и возвращаем курсор
        print(AnsiColor.RESET.value, end='')
        print(AnsiCommand.RESTORE_CURSOR, end='')
        # Нужно переместить курсор в самый низ: RESTORE_CURSOR, как наиболее строгое выполнение условия лабы.