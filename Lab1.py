from Angle import Angle
from AngleRange import AngleRange
from math import pi

a = Angle(pi)
b = Angle(20, in_degrees=True)
c = Angle(365, in_degrees=True)

print("Угол a:", a)
print("Угол b:", b)
print("Угол c:", c)
print(f"Угол c в радианах: {c.radians}")

c.degrees = 10
print("Новый угол c:", c)

print("a > b? ", a > b)
print("b == c? ", b == c)
print("a + b =", a + b)
print("c * 10 =", c * 10)

r1 = AngleRange(0, pi / 2)
r2 = AngleRange(pi / 2, pi, False, True)

print("Диапазон r1:", r1)
print("Диапазон r2:", r2)

print("Длина r1:", r1.length)
print(f"Угол a, {a}, находится в r2?", a in r2)
print("Вычитание диапазонов r2 и r1:", r2 - r1)