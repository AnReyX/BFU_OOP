import math
from typing import Union

class Angle:
    def __init__(self, radians: float = 0.0):
        self._radians = radians
        self._normalize()

    @classmethod
    def from_degrees(cls, degrees: float) -> 'Angle':
        return cls(degrees * math.pi/180)

    def _normalize(self) -> None:
        self._radians = self._radians % (2 * math.pi)

    # - - - Свойства - - -
    @property
    def radians(self) -> float:
        return self._radians

    @radians.setter
    def radians(self, value: float) -> None:
        self._radians = value
        self._normalize()

    @property
    def degrees(self) -> float:
        return math.degrees(self._radians)

    @degrees.setter
    def degrees(self, value: float) -> None:
        self._radians = math.radians(value)
        self._normalize()

    # - - - Преобразования типов - - -
    def __float__(self) -> float:
        return self._radians

    def __int__(self) -> int:
        return int(self._radians)

    def __str__(self) -> str:
        return f"{self.degrees:.3f}°"

    def __repr__(self) -> str:
        return f"Angle({self._radians})"

    # - - - Сравнение - - -
    def __eq__(self, other: Union["Angle", int, float]) -> bool:
        if isinstance(other, Angle):
            return abs(self._radians - other._radians) < 10^-10
        elif isinstance(other, (int, float)):
            return abs(self._radians - other) < 10^-10
        return NotImplemented

    def __lt__(self, other: Union["Angle", int, float]) -> bool:
        if isinstance(other, Angle):
            return self._radians < other._radians
        elif isinstance(other, (int, float)):
            return self._radians < other
        return NotImplemented

    def __le__(self, other: Union["Angle", int, float]) -> bool:
        if isinstance(other, Angle):
            return self._radians <= other._radians
        elif isinstance(other, (int, float)):
            return self._radians <= other
        return NotImplemented

    def __gt__(self, other: Union["Angle", int, float]) -> bool:
        if isinstance(other, Angle):
            return self._radians > other._radians
        elif isinstance(other, (int, float)):
            return self._radians > other
        return NotImplemented

    def __ge__(self, other: Union["Angle", int, float]) -> bool:
        if isinstance(other, Angle):
            return self._radians >= other._radians
        elif isinstance(other, (int, float)):
            return self._radians >= other
        return NotImplemented

    # - - - Арифметика - - -
    def __add__(self, other: Union["Angle", int, float]) -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._radians + other._radians)
        if isinstance(other, (int, float)):
            return Angle(self._radians + other)
        return NotImplemented

    def __sub__(self, other: Union["Angle", int, float]) -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._radians - other._radians)
        if isinstance(other, (int, float)):
            return Angle(self._radians - other)
        return NotImplemented

    def __mul__(self, other: Union[int, float]) -> "Angle":
        return Angle(self._radians * other)

    def __truediv__(self, other: Union[int, float]) -> "Angle":
        return Angle(self._radians / other)