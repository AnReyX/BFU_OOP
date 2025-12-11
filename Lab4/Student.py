from Event import Event
from PropertyChangedEventArgs import PropertyChangedEventArgs
from PropertyChangedEventHandler import PropertyChangedEventHandler
from PropertyChangingEventArgs import PropertyChangingEventArgs
from PropertyChangingEventHandler import PropertyChangingEventHandler


class Student:
    def __init__(self, name: str, study_profile: str, completed_oop_labs: int) -> None:
        self._name = name
        self._study_profile = study_profile
        self._completed_oop_labs = completed_oop_labs
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
    def labs(self) -> int:
        return self._completed_oop_labs
    
    @labs.setter
    def labs(self, new_quantity: int) -> None:
        old_value = self._completed_oop_labs
        self._completed_oop_labs = new_quantity

        self._observer.invoke(self, PropertyChangingEventArgs("_completed_oop_labs", old_value, \
                                                                                       new_quantity, True))
        self._observer.invoke(self, PropertyChangedEventArgs("_completed_oop_labs"))