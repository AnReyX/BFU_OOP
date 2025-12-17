from Event import Event
from PropertyChangedEventArgs import PropertyChangedEventArgs
from PropertyChangedEventHandler import PropertyChangedEventHandler
from PropertyChangingEventArgs import PropertyChangingEventArgs
from PropertyChangingEventHandler import PropertyChangingEventHandler


class Student:
    def __init__(self, name: str, study_profile: str, age: int) -> None:
        self._name = name
        self._study_profile = study_profile
        self._age = age
        self._observer = Event([])
    
    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> None:
        old_value = self._name
        self._name = new_name

        self._observer.invoke(self, PropertyChangingEventArgs("_name", old_value, new_name, False))
        self._observer.invoke(self, PropertyChangedEventArgs("_name"))
    
    @property
    def profile(self) -> str:
        return self._study_profile
    
    @profile.setter
    def profile(self, new_profile: str) -> None:
        old_value = self._study_profile
        self._study_profile = new_profile

        self._observer.invoke(self, PropertyChangingEventArgs("_study_profile", old_value, \
                                                                                       new_profile, True))
        self._observer.invoke(self, PropertyChangedEventArgs("_study_profile"))
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, new_value: int) -> None:
        old_value = self._age
        self._age = new_value

        self._observer.invoke(self, PropertyChangingEventArgs("_age", old_value, new_value, True))
        self._observer.invoke(self, PropertyChangedEventArgs("_age"))