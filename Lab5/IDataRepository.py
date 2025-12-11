from typing import TypeVar, Sequence, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")

class IDataRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        ...
    
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        ...
    
    @abstractmethod
    def add(self, item: T) -> None:
        ...
    
    @abstractmethod
    def update(self, item: T) -> None:
        ...
    
    @abstractmethod
    def delete(self, item: T) -> None:
        ...

