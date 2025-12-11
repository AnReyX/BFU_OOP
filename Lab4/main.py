from House import House
from Student import Student
from PropertyChangedEventHandler import PropertyChangedEventHandler
from PropertyChangingEventHandler import PropertyChangingEventHandler

# пользоваться event примерно так надо, из вне подключая хэндлеров. примерочные классы можно любые задать

handler1 = PropertyChangedEventHandler()
handler2 = PropertyChangingEventHandler()

university = House("Kaliningrad", "Nevskogo", 14)
university._observer += handler1
university._observer += handler2

university.city = "Electrostal'"
print(f'Now city = {university.city}')

university.street = "Novaya"
print(f'Now street = {university.street}')

university.number = 10
print(f'Now number = {university.number}')


student = Student("Andrew", "PM", 3)
student._observer += handler1
student._observer += handler2

student.name = "Nikita"
print(f'Now name = {student.name}')

student.profile = "IB"
print(f'Now profile = {student.profile}')

student.labs = 4
print(f'Now labs = {student.labs}')