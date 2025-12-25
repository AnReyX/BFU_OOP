from abc import ABC, abstractmethod
from typing import Dict
import json


class Command(ABC):
    @abstractmethod
    def execute(self, command_key) -> None:
        pass

    @abstractmethod
    def cancel(self) -> None:
        pass


class WorkingWithText:
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


class Keyboard:
    def __init__(self, save_file: str) -> None:
        self.saving = SaveKeyboardToFile(self, save_file)
        self.output = WorkingWithText()
        self.commands = {}

    def name_commands(self, commands: Dict[str, Command]) -> None:
        self.commands = commands

    def do_commands(self, command_key: str) -> None:
        if command_key not in self.commands:
            print(f"Command '{command_key}' not found")
            return

        command = self.commands[command_key]

        command.execute(command_key)
        self.output.add_command_to_stack(command_key)

    def undo(self) -> None:
        if not self.output.can_undo():
            print('Impossible to undo')
            return

        command_key = self.output.get_index_return_command()
        command = self.commands[command_key]

        command.cancel()

        self.output.index -= 1

    def redo(self) -> None:
        if not self.output.can_redo():
            print('Impossible to redo')
            return

        self.output.index += 1
        command_key = self.output.get_index_return_command()
        command = self.commands[command_key]

        command.execute(command_key)

    def save(self) -> None:
        self.saving.save_to_json()

    def load(self) -> None:
        self.saving.load_from_json()


class KeyCommand(Command):
    def __init__(self, keyboard: Keyboard) -> None:
        self.keyboard = keyboard

    def execute(self, command_key) -> None:
        self.keyboard.output.add_letter(command_key)
        print(self.keyboard.output.text)

    def cancel(self) -> None:
        self.keyboard.output.remove_last_letter()
        print(self.keyboard.output.text)


class VolumeUpCommand(Command):
    def execute(self, command_key) -> None:
        print("volume increased 20%")

    def cancel(self) -> None:
        print("volume decreased 20%")


class VolumeDownCommand(Command):
    def execute(self, command_key) -> None:
        print("volume decreased 20%")

    def cancel(self) -> None:
        print("volume increased 20%")


class MediaPlayerCommand(Command):
    def execute(self, command_key) -> None:
        print("Media Player started")

    def cancel(self) -> None:
        print("Media Player closed")


class SaveKeyboardToFile:
    def __init__(self, keyboard: Keyboard, file_dir: str):
        self.keyboard = keyboard
        self.file_dir = file_dir

    def save_to_json(self) -> None:
        commands_info = {}
        for key, value in self.keyboard.commands.items():
            commands_info[key] = value.__class__.__name__

        data = {
            "text": self.keyboard.output.text,
            "commands_stack": self.keyboard.output.commands_stack,
            "index": self.keyboard.output.index,
            "commands": commands_info
        }

        try:
            with open(self.file_dir, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Keyboard saved to {self.file_dir}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def load_from_json(self) -> None:
        try:
            with open(self.file_dir, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading file: {e}")
            return

        self.keyboard.output.text = data.get("text", "")
        self.keyboard.output.commands_stack = data.get("commands_stack", [])
        self.keyboard.output.index = data.get("index", -1)

        commands_info = data.get("commands", {})
        restored_commands = {}

        available_classes = globals()

        for key, class_name in commands_info.items():
            if class_name in available_classes:
                command_class = available_classes[class_name]

                if class_name == "KeyCommand":
                    restored_commands[key] = command_class(self.keyboard)
                else:
                    restored_commands[key] = command_class()
            else:
                print(f"Class {class_name} not found")

        self.keyboard.commands = restored_commands
        print(f"Keyboard loaded from {self.file_dir}")


k = Keyboard("keyboard_state.json")

commands = {
    'b': KeyCommand(k),
    'l': KeyCommand(k),
    'o': KeyCommand(k),
    'h': KeyCommand(k),
    'a': KeyCommand(k),
    'ctrl+V++': VolumeUpCommand(),
    'ctrl+D+-': VolumeDownCommand(),
    'ctrl+S': MediaPlayerCommand(),
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
k2 = Keyboard("keyboard_state.json")
k2.load()

print(f"Написанный текст: {k2.output.text}")
print(f"Загруженный stack: {k2.output.commands_stack}")

print("\n7. Добавим новую команду:")

if 's' not in k2.commands:
    k2.commands['s'] = KeyCommand(k2)
k2.do_commands('s')