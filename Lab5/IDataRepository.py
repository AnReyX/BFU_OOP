from typing import TypeVar, Generic, Sequence, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')


class IDataRepository(ABC, Generic[T]):
    """
    Интерфейс CRUD репозитория.
    """

    @abstractmethod
    def get_all(self) -> Sequence[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass