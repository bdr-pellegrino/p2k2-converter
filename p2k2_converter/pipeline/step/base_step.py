from typing import TypeVar
from abc import ABC, abstractmethod
from p2k2_converter.pipeline.source import BaseSource

T = TypeVar('T')
Q = TypeVar('Q')


class BaseStep(ABC):
    def __init__(self, name: str):
        self.__name = name
        self.__next = None

    def get_name(self):
        return self.__name

    def set_next(self, next_step: 'BaseStep'):
        self.__next = next_step

    def run(self, source: BaseSource, data: any) -> list[T, Q]:
        execution_result = self.execute(source, data)
        if self.__next is None:
            return execution_result
        else:
            source, data = execution_result
            return self.__next.run(source, data)

    @abstractmethod
    def execute(self, source: BaseSource, data: any) -> list[T, Q]:
        pass
