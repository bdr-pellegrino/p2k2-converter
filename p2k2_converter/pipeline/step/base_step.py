from typing import TypeVar
from abc import ABC, abstractmethod
T = TypeVar('T')


class BaseStep(ABC):
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def execute(self) -> T:
        pass
