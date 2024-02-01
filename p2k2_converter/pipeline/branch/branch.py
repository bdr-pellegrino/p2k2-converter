from copy import deepcopy as copy

from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import BaseStep, DataExtractor
from typing import TypeVar

T = TypeVar("T")
Q = TypeVar("Q")


class Branch:
    def __init__(self, name: str, steps: list[BaseStep] = None):
        self.__starting_step = None
        self.__last_step = None
        if steps is not None:
            for step in steps:
                self.add_step(step)

        self.__name = name
        self.__executed = False
        self.__data: T = None
        self.__result: Q = None

    def add_step(self, step: BaseStep) -> None:
        if self.__starting_step is None:
            self.__starting_step = step
            self.__last_step = step
        else:
            self.__last_step.set_next(step)
            self.__last_step = step

    def get_name(self) -> str:
        return self.__name

    def get_data(self) -> T:
        if not self.__executed:
            raise RuntimeError("Branch not executed yet")
        return copy(self.__data)

    def get_result(self) -> Q:
        if not self.__executed:
            raise RuntimeError("Branch not executed yet")
        return copy(self.__result)

    def execute(self, source: BaseSource) -> T:
        if self.__executed:
            raise RuntimeError("Branch already executed")

        if self.__starting_step is None:
            raise RuntimeError("Branch has no steps")

        self.__data, self.__result = self.__starting_step.run(source, None)
        self.__executed = True
        return self.__result
