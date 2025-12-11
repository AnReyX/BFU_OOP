from typing import List, Union
from Angle import Angle

class AngleRange:
    def __init__(self, start: Union[Angle, int, float], end: Union[Angle, int, float],
                 inc_start: bool = True, inc_end: bool = True):
        self.start = start if isinstance(start, Angle) else Angle(start)
        self.end = end if isinstance(end, Angle) else Angle(end)
        self.inc_start = inc_start
        self.inc_end = inc_end

    # --- Строковые представления ---
    def __str__(self) -> str:
        s = "[" if self.inc_start else "("
        e = "]" if self.inc_end else ")"
        return f"{s}{self.start.degrees:.2f}°; {self.end.degrees:.2f}°{e}"

    def __repr__(self) -> str:
        return (f"AngleRange({repr(self.start)}, {repr(self.end)}, "
                f"inc_start={self.inc_start}, inc_end={self.inc_end})")

    # - - - Длина диапазона - - -
    def __abs__(self) -> float:
        return self.start.radians - self.end.radians

    # - - - Сравнения - - -
    def __eq__(self, other: 'AngleRange') -> bool:
        return (self.start == other.start and self.end == other.end and self.inc_start == other.inc_start and
                self.inc_end == other.inc_end)

    def __ne__(self, other: 'AngleRange') -> bool:
        return not self == other
    

    def __lt__(self, other: 'AngleRange') -> bool:
        if self.end == other.end and not self.inc_end and other.inc_end:
            return True
        return self.end < other.end

    def __le__(self, other: 'AngleRange') -> bool:
        return (self < other) or (self == other)

    def __gt__(self, other: 'AngleRange') -> bool:
        if self.end == other.end and self.inc_end and not other.inc_end:
            return True
        return self.end > other.end

    def __ge__(self, other: 'AngleRange') -> bool:
        return (self > other) or (self == other)


    # - - - Проверка принадлежности угла - - -
    def contains_angle(self, a: Angle) -> bool:
        x = a.radians
        s = self.start.radians
        e = self.end.radians

        if self.inc_start and x == s:
            return True
        if self.inc_end and x == e:
            return True
        return s < x < e
    
    
    # - - - Содержит другой диапазон - - -
    def contains_range(self, other: "AngleRange") -> bool:
        return ((self.start.radians <= other.start.radians if
                 (self.inc_start or not self.inc_start and not other.inc_start)
                 else self.start.radians < other.start.radians) and
                (self.end.radians >= other.end.radians if (self.inc_end or not self.inc_end and not other.inc_end)
                 else self.end.radians > other.end.radians))

    def __contains__(self, item: Union['AngleRange', Angle, int, float]) -> bool:
        if isinstance(item, Angle):
            return self.contains_angle(item)
        if isinstance(item, (int, float)):
            return self.contains_angle(Angle(item))
        if isinstance(item, AngleRange):
            return self.contains_range(item)
        return NotImplemented

    # - - - Сложение диапазонов - - -
    def __add__(self, other: "AngleRange") -> List["AngleRange"]:
        if self.end < other.start: # Не пересекаются
            return [self, other]
        if other.end < self.start:
            return [other, self]
        if self.end == other.start: # Пересекаются по одной точке
            if not self.inc_end and self.inc_end == other.inc_start:
                return [self, other]
            return [AngleRange(self.start, other.end, self.inc_start, other.inc_end)]
        if other.end == self.start:
            if not self.inc_start and other.inc_end == self.inc_start:
                return [other, self]
            return [AngleRange(other.start, self.end, other.inc_start, self.inc_end)]
        if self.start == other.start and self.end == other.end: # Совпали полностью
            return [AngleRange(self.start, self.end, self.inc_start or other.inc_start, self.inc_end or other.inc_end)]
        if self.start == other.start: # Совпали начала
            if self.end > other.end:
                return [AngleRange(self.start, self.end, self.inc_start or other.inc_start, self.inc_end)]
            return [AngleRange(self.start, other.end, self.inc_start or other.inc_start, other.inc_end)]
        if self.end == other.end: # Совпали концы
            if self.start > other.start:
                return [AngleRange(other.start, self.end, other.inc_start, self.inc_end or other.inc_end)]
            return [AngleRange(self.start, self.end, self.inc_start, self.inc_end or other.inc_end)]
        if self.start < other.start and other.end < self.end: # Вложенные отрезки
            return [self]
        if other.start < self.start and self.end < other.end:
            return [other]
        if self.end > other.start and self.start < other.end: # Пересечение по отрезку
            return [AngleRange(self.start, other.end, self.inc_start, other.inc_end)]
        if other.end > self.start and other.start < self.end:
            return [AngleRange(other.start, self.end, other.inc_start, self.inc_end)]
        return [self]

    # - - - Вычитание диапазонов - - -
    def __sub__(self, other: "AngleRange") -> List["AngleRange"]:
        result: List[AngleRange] = [] # Пустой список, если self полностью лежит в other

        if not (self.contains_angle(other.start) or self.contains_angle(other.end)): # Не пересекаются
            return [self]

        if self.contains_angle(other.start) and self.start != other.start:
            result.append(AngleRange(self.start, other.start, self.inc_start, not other.inc_start))

        if self.contains_angle(other.end) and self.end != other.end:
            result.append(AngleRange(other.end, self.end, not other.inc_end, self.inc_end))

        if self.contains_angle(other.start) and self.start == other.start and not other.inc_start:
            result.append(AngleRange(self.start, self.start, True, True))

        if self.contains_angle(other.end) and self.end == other.end and not other.inc_end:
            result.append(AngleRange(self.end, self.end, True, True))

        return result