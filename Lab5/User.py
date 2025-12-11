from dataclasses import dataclass
from dataclasses import field
from typing import Self


@dataclass
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    address: str | None = None
    email: str | None = None

    def __lt__(self, other: Self) -> bool:
        return self.name < other.name
    
    def __gt__(self, other: Self) -> bool:
        return self.name > other.name


