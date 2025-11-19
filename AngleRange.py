from typing import List
from math import pi

from Angle import Angle


class AngleRange:
    """
    - Реализовать механизм создания объекта через задание начальной и конечной точки промежутка в виде углов float,
     int или Angle
    - Предусмотреть возможность использования включающих и исключающих промежутков
    - реализовать возможность сравнения объектов на эквивалентность (eq)
    - реализовать строковое представление объекта (str, repr)
    - реализовать получение длины промежутка (abs или отдельны метод)
    - реализовать сравнение промежутков
    - реализовать операцию in для проверки входит один промежуток в другой или угол в промежуток
    - реализовать операции сложения, вычитания (результат в общем виде - список промежутков)
    """

    def __init__(self, start, end, inclusive_start: bool = True, inclusive_end: bool = True) -> None:
        self.start = start if isinstance(start, Angle) else Angle(start)
        self.end = end if isinstance(end, Angle) else Angle(end)
        self.inc_start = inclusive_start
        self.inc_end = inclusive_end

    # --- Строковые представления ---
    def __str__(self) -> str:
        s = "[" if self.inc_start else "("
        e = "]" if self.inc_end else ")"
        return f"{s}{self.start.degrees:.2f}°; {self.end.degrees:.2f}°{e}"

    def __repr__(self) -> str:
        return (f"AngleRange({repr(self.start)}, {repr(self.end)}, "
                f"inc_start={self.inc_start}, inc_end={self.inc_end})")

    # --- Длина диапазона ---
    @property
    def length(self) -> float:
        s = self.start.radians
        e = self.end.radians
        if e >= s:
            return e - s
        return 2 * pi + e - s

    # --- Равенство ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        return (self.start == other.start and
                self.end == other.end and
                self.inc_start == other.inc_start and
                self.inc_end == other.inc_end)

    # --- Проверка принадлежности угла ---
    def contains_angle(self, a: Angle) -> bool:
        x = a.radians
        s = self.start.radians
        e = self.end.radians

        if s < e:
            if self.inc_start and x == s:
                return True
            if self.inc_end and x == e:
                return True
            return s < x < e

        if x > s or x < e:
            return True
        if self.inc_start and x == s:
            return True
        if self.inc_end and x == e:
            return True
        return False

    def __contains__(self, item) -> bool:
        if isinstance(item, Angle):
            return self.contains_angle(item)
        if isinstance(item, (int, float)):
            return self.contains_angle(Angle(item))
        return False

    # --- Содержит другой диапазон ---
    def contains_range(self, other: "AngleRange") -> bool:
        return (self.contains_angle(other.start) and
                self.contains_angle(other.end))

    # --- Сложение диапазонов ---
    def __add__(self, other: "AngleRange") -> List["AngleRange"]:
        if self.contains_angle(other.start) or other.contains_angle(self.start):
            return [AngleRange(self.start, other.end)]
        return [self, other]

    # --- Вычитание диапазонов ---
    def __sub__(self, other: "AngleRange") -> List["AngleRange"]:
        result: List[AngleRange] = []

        if not (self.contains_angle(other.start) or
                self.contains_angle(other.end)):
            return [self]

        if self.contains_angle(other.start) and self.start != other.start:
            result.append(
                AngleRange(self.start, other.start, self.inc_start, False)
            )

        if self.contains_angle(other.end) and self.end != other.end:
            result.append(
                AngleRange(other.end, self.end, False, self.inc_end)
            )

        return result