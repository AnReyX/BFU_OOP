from typing import TypeVar, Generic
from abc import ABC, abstractmethod

TEventArgs = TypeVar("TEventArgs")

class EventHandler(Generic[TEventArgs], ABC):
    @abstractmethod
    def handle(self, sender: object, args: TEventArgs) -> None:
        pass