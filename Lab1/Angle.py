from __future__ import annotations
import math
from typing import Union


class Angle:
    def __init__(self, radians: float = 0.0):
        self._radians = radians

    @classmethod
    def from_degrees(cls, degrees: float) -> Angle:
        return cls(math.radians(degrees))

    @staticmethod
    def normalize(radians: float) -> float:
        return radians % (2 * math.pi)

    # - - - Свойства - - -
    @property
    def radians(self) -> float:
        return self._radians

    @radians.setter
    def radians(self, value: float) -> None:
        self._radians = value

    @property
    def degrees(self) -> float:
        return math.degrees(self._radians)

    @degrees.setter
    def degrees(self, value: float) -> None:
        self._radians = math.radians(value)

    # - - - Преобразования типов - - -
    def __float__(self) -> float:
        return self._radians

    def __int__(self) -> int:
        return int(self.degrees)

    def __str__(self) -> str:
        return f"{self.degrees:.3f}°"

    def __repr__(self) -> str:
        return f"Angle({self._radians})"

    # - - - Сравнение - - -
    def __eq__(self, other: Union[Angle, int, float]) -> bool:
        angle_s = Angle.normalize(self._radians)
        if isinstance(other, Angle):
            angle_o = Angle.normalize(other._radians)
            return abs(angle_s - angle_o) < 10 ** -10
        elif isinstance(other, (int, float)):
            angle_o = Angle.normalize(other)
            return abs(angle_s - angle_o) < 10 ** -10
        return NotImplemented

    def __lt__(self, other: Union[Angle, int, float]) -> bool:
        angle_s = Angle.normalize(self._radians)
        if isinstance(other, Angle):
            angle_o = Angle.normalize(other._radians)
            return angle_s < angle_o
        elif isinstance(other, (int, float)):
            angle_o = Angle.normalize(other)
            return angle_s < angle_o
        return NotImplemented

    def __le__(self, other: Union[Angle, int, float]) -> bool:
        return (self < other) or (self == other)

    def __gt__(self, other: Union[Angle, int, float]) -> bool:
        angle_s = Angle.normalize(self._radians)
        if isinstance(other, Angle):
            angle_o = Angle.normalize(other._radians)
            return angle_s > angle_o
        elif isinstance(other, (int, float)):
            angle_o = Angle.normalize(other)
            return angle_s > angle_o
        return NotImplemented

    def __ge__(self, other: Union[Angle, int, float]) -> bool:
        return (self > other) or (self == other)

    # - - - Арифметика - - -
    def __add__(self, other: Union[Angle, int, float]) -> "Angle":
        if isinstance(other, Angle):
            return Angle(self._radians + other._radians)
        if isinstance(other, (int, float)):
            return Angle(self._radians + other)
        return NotImplemented

    def __sub__(self, other: Union[Angle, int, float]) -> "Angle":
        if isinstance(other, Angle):
            return Angle(abs(self._radians - other._radians))
        if isinstance(other, (int, float)):
            return Angle(abs(self._radians - other))
        return NotImplemented

    def __mul__(self, other: Union[int, float]) -> "Angle":
        return Angle(self._radians * other)

    def __truediv__(self, other: Union[int, float]) -> "Angle":
        return Angle(self._radians / other)

# [pi / 3, 7 * pi] in [ pi / 6, 8 * pi] = True