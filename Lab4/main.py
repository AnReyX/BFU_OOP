from House import House
from Student import Student
from PropertyChangedEventHandler import PropertyChangedEventHandler
from PropertyChangingEventHandler import PropertyChangingEventHandler
from PropertyChangingMaxLenHandler import PropertyChangingMaxLenHandler

handler1 = PropertyChangedEventHandler()
handler2 = PropertyChangingEventHandler()
handler3 = PropertyChangingMaxLenHandler()

'''
university = House("Kaliningrad", "Nevskogo", 14)
university.add_handler(handler1)
university.add_handler(handler2)

university.city = "Electrostal'"
print(f'Now city = {university.city}')

university.street = "Novaya"
print(f'Now street = {university.street}')

university.number = 10
print(f'Now number = {university.number}')


student = Student("Andrew", "PM", 19)
student.add_handler(handler1)
student.add_handler(handler2)

student.name = "Nikita"
print(f'Now name = {student.name}')

student.profile = "IB"
print(f'Now profile = {student.profile}')

student.age = 20
print(f'Now age = {student.age}')
'''

student2 = Student("Victor", "PM", 18)
student2.add_handler(handler1)
student2.add_handler(handler3)

student2.name = "Yan"
print(f'Now name = {student2.name}')

student2.profile = "IB"
print(f'Now profile = {student2.profile}')

student2.age = 19
print(f'Now age = {student2.age}')
