from typing import TypeVar

T = TypeVar('T')

class BaseStep:
    def __init__(self, name: str):
        self.__name = name

    def name(self) -> str:
        """
        Returns the name of the step.
        """
        ...

    def execute(self) -> T:
        """
        Executes the step
        :return: The result of the step.
        """
        ...
