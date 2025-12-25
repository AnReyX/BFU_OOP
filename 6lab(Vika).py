from abc import ABC, abstractmethod
from typing import Dict
import openpyxl
import ast


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass


class WorkingWithText():
    def __init__(self):
        self.commands_stack = []
        self.index = -1
        self.text = ""

    def add_letter(self, char: str) -> None:
        self.text += char
    
    def remove_last_letter(self) -> None:
        if self.text:
            self.text = self.text[:-1]
    
    def add_command_to_stack(self, command_key: str) -> None:
        self.commands_stack.append(command_key)
        self.index += 1
    
    def cut_stack(self, index: int) -> None:
        self.commands_stack = self.commands_stack[:index + 1]
    
    def get_index_return_command(self) -> str:
        return self.commands_stack[self.index]
    
    def can_undo(self) -> bool:
        return self.index >= 0
    
    def can_redo(self) -> bool:
        return self.index < len(self.commands_stack) - 1


class Keyboard():
    def __init__(self, save_file: str) -> None:
        self.saving = SaveKeyboardToFile(self, save_file)
        self.output = WorkingWithText()
        self.commands = {}

    def name_commands(self,commands: Dict[str, Command]) -> None:
        self.commands = commands

    def do_commands(self, command_key: str) -> None:
        if command_key not in self.commands:
            print(f"Command '{command_key}' not found")
            return

        command = self.commands[command_key]
        
        if isinstance(command, KeyCommand):
            self.output.add_letter(command_key)

        command.execute()
        self.output.add_command_to_stack(command_key)

    def undo(self) -> None:
        if not self.output.can_undo():
            print('Impossible to undo')
            return

        command_key = self.output.get_index_return_command()
        command = self.commands[command_key]
        
        if isinstance(command, KeyCommand):
            self.output.remove_last_letter()

        command.cancel()
        
        self.output.index -= 1

    def redo(self) -> None:
        if not self.output.can_redo():
            print('Impossible to redo')
            return

        self.output.index += 1
        command_key = self.output.get_index_return_command()
        command = self.commands[command_key]
        
        if isinstance(command, KeyCommand):
            self.output.add_letter(command_key)
        
        command.execute()

    def save(self) -> None:
        self.saving.save_to_xlsx()

    def load(self) -> None:
        self.saving.load_from_xlsx()


class KeyCommand(Command):
    def __init__(self, keyboard: Keyboard) -> None:
        self.keyboard = keyboard

    def execute(self) -> None:
        print(self.keyboard.output.text)

    def cancel(self) -> None:
        print(self.keyboard.output.text)

    def is_printed(self) -> bool:
        return True
    

class VolumeUpCommand(Command):
    def execute(self) -> None:
        print("volume increased 20%")

    def cancel(self) -> None:
        print("volume decreased 20%")


class VolumeDownCommand(Command):
    def execute(self) -> None:
        print("volume decreased 20%")

    def cancel(self) -> None:
        print("volume increased 20%")

    
class StardewValleyPlayerCommand(Command):
    def execute(self) -> None:
        print("Stardew valley started")

    def cancel(self) -> None:
        print("Stardew valley closed")


class SaveKeyboardToFile():
    def __init__(self, keyboard: Keyboard, file_dir: str):
        self.keyboard = keyboard
        self.file_dir = file_dir

    def save_to_xlsx(self) -> None:
        wb = openpyxl.Workbook()
        note = wb.active

        note['A1'] = "Field"
        note['B1'] = "Value"

        note['A2'] = "text"
        note['B2'] = self.keyboard.output.text

        note['A3'] = "commands stack"
        note['B3'] = str(self.keyboard.output.commands_stack)

        note['A4'] = "index"
        note['B4'] = str(self.keyboard.output.index)

        note['A6'] = "Command key"
        note['B6'] = "Command value"
        
        row = 7
        for key, value in self.keyboard.commands.items():
            note[f'A{row}'] = key
            note[f'B{row}'] = value.__class__.__name__
            row += 1 

        wb.save(self.file_dir)
        print(f"Keyboard saved to {self.file_dir}")

    def load_from_xlsx(self) -> None:
        try:
            wb = openpyxl.load_workbook(self.file_dir)
        except FileNotFoundError:
             return print(f"File {self.file_dir} not found")
        
        note = wb.active
        self.keyboard.output.text = note['B2'].value 

        commands_stack_str = note['B3'].value 
        self.keyboard.output.commands_stack = ast.literal_eval(commands_stack_str)

        index_str = note['B4'].value 
        self.keyboard.output.index = ast.literal_eval(index_str)

        commands = {}
        row = 7

        while note[f'A{row}'].value:
            key = note[f'A{row}'].value
            class_name = note[f'B{row}'].value

            try:
                command_class = getattr(__import__(__name__), class_name)
                if class_name == "KeyCommand":
                    commands[key] = command_class(self.keyboard)
                else:
                    commands[key] = command_class()
            except AttributeError:
                print(f"not found {class_name}")
            row += 1
        
        self.keyboard.commands = commands
        print(f"Keboard loaded from {self.file_dir}")
                    

k = Keyboard("keyboard_state.xlsx")
    
commands = {
    'b': KeyCommand(k),
    'l': KeyCommand(k),
    'o': KeyCommand(k),
    'h': KeyCommand(k),
    'a': KeyCommand(k),
    'ctrl+V++': VolumeUpCommand(),
    'ctrl+D+-': VolumeDownCommand(),
    'ctrl+S': StardewValleyPlayerCommand(),
}

k.name_commands(commands)

print("\n1: Печать символов")
k.do_commands('b')
k.do_commands('l')
k.do_commands('o')
k.do_commands('h')
k.do_commands('a')

print(f"\nИтоговый текст: {k.output.text}")

print("\n2. Undo:")
k.undo()
k.undo()

print("\n3. Redo:")
k.redo()
k.redo()

print("\n4. Команды со звуком / и не только:")
k.do_commands('ctrl+V++')
k.do_commands('ctrl+S')

print("\n5. Сохранение состояния")
k.save()

print("\n6. Используем сохраненное состояние:")
k2 = Keyboard("keyboard_state.xlsx")
k2.load()

print(f"Написанный текст: {k2.output.text}")
print(f"Загруженный stack: {k2.output.commands_stack}")

print("\n7. Добавим новую команду:")
k2.do_commands('s')
k2.commands['s'] = KeyCommand(k2)
k2.do_commands('s')