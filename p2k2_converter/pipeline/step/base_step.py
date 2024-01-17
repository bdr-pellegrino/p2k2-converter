from typing import TypeVar

T = TypeVar('T')


class BaseStep:
    def __init__(self, name):
        self.__name = name

    def name(self):
        return self.__name

    def execute(self) -> T:
        pass
