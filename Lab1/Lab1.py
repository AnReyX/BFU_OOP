from Angle import Angle
from AngleRange import AngleRange
from math import pi

a = Angle(pi)
b = Angle.from_degrees(20)
c = Angle.from_degrees(365)

print(f"Угол a: {a.degrees} градусов")
print(f"Угол b: {b.radians} радиан")
print("Угол c:", c)

c.degrees = 10
print("Новый угол c:", c)
print(f"Целочисленный b: {int(b)} радиан")

print("a > b? ", a > b)
print("b == c? ", b == c)
print("a + b =", a + b)
print("c - a =", c - a)
print("c * 10 =", c * 10)
print("b / 2.5 =", b / 2.5, "\n")

r1 = AngleRange(0, pi / 2)
r2 = AngleRange(c, a, False, True)
r3 = AngleRange(c, pi, False, False)

print("Диапазон r1:", r1)
print("Диапазон r2:", r2)
print("Диапазон r3:", r3)

print("Длина r1:", abs(r1))
print(f"Угол b, {b}, находится в r2?", b in r2)
print("Диапазон r2 равен диапазону r3?", r2 == r3)
print("Диапазон r2 содержит диапазон r1?", r1 in r2)
print("Сложение диапазонов r1 и r3:", r1 + r3)
print("Вычитание диапазонов r2 и r3:", r2 - r3)