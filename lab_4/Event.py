from EventHandler import EventHandler
from typing import TypeVar, Self


TEventArgs = TypeVar("TEventArgs")
T = TypeVar("T")


class Event:
    def __init__(self, handlers: list[EventHandler]) -> None:
        self._handlers: list[EventHandler] = handlers

    def __iadd__(self, handler: EventHandler) -> Self:
        self._handlers.append(handler)
        return self
    
    def __isub__(self, handler: EventHandler) -> Self:
        self._handlers.remove(handler)
        return self
    
    def invoke(self, sender: T, args: TEventArgs) -> None:
        for handler in self._handlers:
            handler.handle(sender, args)
    
