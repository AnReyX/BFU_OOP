from typing import Callable, Any, Optional
from enum import Enum
import inspect
from abc import ABC, abstractmethod


class LifeStyle(Enum):
    PerRequest = "PerRequest"
    Scoped = "Scoped"
    Singleton = "Singleton"


class Injector:
    def __init__(self) -> None:
        self.registrations = {}
        self.singletons = {}
        self.scopes = []

    def register(self, interface: object, cls_func: object | Callable, 
                 lifestyle: Optional[LifeStyle] = None, 
                 parameters: Optional[dict[str, Any]] = None) -> None:
        if inspect.isclass(cls_func):
            sig = inspect.signature(cls_func.__init__)
            for name, parameter in sig.parameters.items():
                if name == "self":
                    continue
                if parameter.annotation != inspect.Parameter.empty and parameter.annotation not in self.registrations:
                    raise Exception(f"You should registrate '{parameter.annotation}'")
        self.registrations[interface] = {
            'target': cls_func,
            'lifestyle': lifestyle,
            'parameters': parameters if parameters else {}
        }

    def get_instance(self, interface: type) -> Any:
        if interface not in self.registrations:
            raise KeyError(f"Interface '{interface}' not registered")
        
        reg = self.registrations[interface]
        target = reg["target"]
        parameters = reg["parameters"]
        lifestyle = reg["lifestyle"]

        if lifestyle == LifeStyle.Singleton and interface in self.singletons:
            return self.singletons[interface]
        
        if lifestyle == LifeStyle.Scoped and self.scopes and interface in self.scopes[-1]:
            return self.scopes[-1][interface]

        if inspect.isclass(target):
            sign = inspect.signature(target.__init__)
            args = {}

            for name, parameter in sign.parameters.items():
                if name in ["self", "args", "kwargs"]:
                    continue
                if name in parameters:
                    args[name] = parameters[name]
                elif parameter.annotation != inspect.Parameter.empty and parameter.annotation in self.registrations:
                    args[name] = self.get_instance(parameter.annotation)
                elif parameter.default != inspect.Parameter.empty:
                    args[name] = parameter.default
                else:
                    raise Exception(f"Cannot resolve parameter '{name}'")

            obj = target(**args)
        else:
            obj = target(**parameters)

        if lifestyle == LifeStyle.Singleton:
            self.singletons[interface] = obj
        elif lifestyle == LifeStyle.Scoped:
            if not self.scopes:
                raise Exception("No active scope")
            self.scopes[-1][interface] = obj
        return obj
    
    def open_scope(self) -> object:
        return Scope(self)
    

class Scope:
    def __init__(self, injector: Injector) -> None:
        self.injector = injector

    def __enter__(self) -> Injector:
        self.injector.scopes.append({})
        return self.injector
    
    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.injector.scopes.pop()


class interface1:
  pass
class interface2:
  pass
class interface3:
  pass


class class1_debug(interface1):
    def __init__(self):
        print("Created class1_debug")
        self.name = "class1_debug"


class class1_release(interface1):
    def __init__(self):
        print("Created class1_release")
        self.name = "class1_release"


class class2_debug(interface2):
    def __init__(self, i1: interface1):
        print("Created class2_debug")
        self.i1 = i1
        self.name = "class2_debug"


class class2_release(interface2):
    def __init__(self, i1: interface1):
        print("Created class2_release")
        self.i1 = i1
        self.name = "class2_release"


class class3_debug(interface3):
    def __init__(self, i1: interface1, i2: interface2):
        print("Created class3_debug")
        self.i1 = i1
        self.i2 = i2
        self.name = "class3_debug"


class class3_release(interface3):
    def __init__(self, i1: interface1, i2: interface2):
        print("Created class3_release")
        self.i1 = i1
        self.i2 = i2
        self.name = "class3_release"


print("Configuration 1: debug")
injector = Injector()
injector.register(interface1, class1_debug, LifeStyle.PerRequest)
injector.register(interface2, class2_debug, LifeStyle.PerRequest)
injector.register(interface3, class3_debug, LifeStyle.PerRequest)

print("\nCreating objects:")
obj1 = injector.get_instance(interface1)
obj2 = injector.get_instance(interface2)
obj3 = injector.get_instance(interface3)

print(f"\nOutput:")
print(f"obj1.name: {obj1.name}")
print(f"obj2.name: {obj2.name}, obj2.i1.name: {obj2.i1.name}")
print(f"obj3.name: {obj3.name}, obj3.i1.name: {obj3.i1.name}, obj3.i2.name: {obj3.i2.name}")

print("\nConfiguration 2: different Lifestyles")
injector = Injector()
injector.register(interface1, class1_release, LifeStyle.Singleton)
injector.register(interface2, class2_release, LifeStyle.Scoped)
injector.register(interface3, class3_release, LifeStyle.PerRequest)

print("\nSingleton test:")
s1 = injector.get_instance(interface1)
s2 = injector.get_instance(interface1)
print(f"s1 is s2: {s1 is s2}")

print("\nScoped test:")
with injector.open_scope():
    sc1 = injector.get_instance(interface2)
    sc2 = injector.get_instance(interface2)
    print(f"Inside scope: sc1 is sc2: {sc1 is sc2}")

with injector.open_scope():
    sc3 = injector.get_instance(interface2)
    print(f"New scope: sc1 is sc3: {sc1 is sc3}")

print("\nPerRequest test:")
with injector.open_scope():
    pr1 = injector.get_instance(interface3)
    pr2 = injector.get_instance(interface3)
    print(f"pr1 is pr2: {pr1 is pr2}")

# class func(ABC):
#     @abstractmethod
#     def aaaa(self) -> None:
#         pass
#
#     def mes(self) -> str:
#         pass
#
# class func_2(func):
#     def aaaa(self) -> None:
#         pass
#
#     def mes(self) -> str:
#         pass
#
# def fabric_method(mes: str) -> func:
#     return func_2(mes = mes)
#
# injector = Injector()
# injector.register(func, fabric_method, LifeStyle.Singleton, parameters = {"mes": ":("})