from dataclasses import dataclass, field
from typing import Optional, Self

@dataclass
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: Optional[str] = None
    address: Optional[str] = None

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.name < other.name

    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.name > other.name