from ANSI import AnsiColor, AnsiCommand
from Printer import Printer


# Очистим экран для красоты
print(AnsiCommand.CLEAR_SCREEN, end='')

# Статически выведем "HELLO" красным цветом, символом '#', в позиции (100, 10), шрифтом font5.json (высоты 5)
Printer.print_static(
    text="HELLO",
    color=AnsiColor.RED,
    position=(100, 10),
    symbol="#",
    font_path="font5.json"
)

# Используем экземпляр и with (Context Manager). Выводим текст синим цветом, символом '@', начиная с позиции (10, 5)
# Шрифт font7.json (высоты 7)

with Printer(AnsiColor.BLUE, (10, 5), "@", "font7.json") as printer:
    printer.print("WORLD")
    printer.print("WRD2") # Выводится ниже предыдущего автоматически

print(AnsiCommand.move_cursor(1, 25)) # Переместим курсор ниже, чтоб системные сообщения не затерли рисунок
print("Работа завершена.")