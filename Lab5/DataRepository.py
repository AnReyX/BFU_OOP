from IDataRepository import IDataRepository
from typing import TypeVar, Sequence, List, Optional, Type
from dataclasses import asdict
import os
import json

T = TypeVar('T')

class DataRepository(IDataRepository[T]):

    def __init__(self, filename: str, cls: Type[T]):
        self.filename = filename
        self.cls = cls
        self._data: List[T] = self._load_from_file()

    def _load_from_file(self) -> List[T]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, encoding='utf-8') as f:
                data_list = json.load(f)
                return [self.cls(**item) for item in data_list]
        except Exception:
            return []

    def _save_to_file(self) -> None:
        data_to_save = [asdict(item) for item in self._data]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)

    def get_all(self) -> Sequence[T]:
        return self._data

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._data:
            if getattr(item, 'id', None) == id:
                return item
        return None

    def add(self, item: T) -> None:
        self._data.append(item)
        self._save_to_file()

    def update(self, item: T) -> None:
        target_id = getattr(item, 'id', None)
        for i, existing_item in enumerate(self._data):
            if getattr(existing_item, 'id', None) == target_id:
                self._data[i] = item
                self._save_to_file()
                return

    def delete(self, item: T) -> None:
        target_id = getattr(item, 'id', None)
        self._data = [i for i in self._data if getattr(i, 'id', None) != target_id]
        self._save_to_file()