from copy import deepcopy as copy

from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import BaseStep, DataExtractor
from typing import TypeVar

T = TypeVar("T")


class Branch:
    def __init__(self, name: str, steps: list[BaseStep] = None):
        self.__steps = {
            "extractor": None,
            "mappers": {},
        }

        if steps is not None:
            for step in steps:
                if isinstance(step, DataExtractor):
                    self.__steps["extractor"] = step
                else:
                    self.__steps["mappers"][step.get_name()] = step

        self.__name = name
        self.__executed = False
        self.__data: T = None

    def add_step(self, step: BaseStep, force: bool = False) -> None:
        if isinstance(step, DataExtractor):
            if self.__steps["extractor"] is not None and not force:
                raise ValueError("DataExtractor already set for this branch")
            self.__steps["extractor"] = step
        else:
            if step.get_name() in self.__steps["mappers"] and not force:
                raise ValueError("DataMapper already set for this branch")
            self.__steps["mappers"][step.get_name()] = step

    def get_name(self) -> str:
        return self.__name

    def get_data(self) -> T:
        if not self.__executed:
            raise RuntimeError("Branch not executed yet")
        return copy(self.__data)

    def get_steps(self) -> dict[str, BaseStep]:
        return copy(self.__steps)

    def execute(self, source: BaseSource) -> T:
        if self.__executed:
            raise RuntimeError("Branch already executed")

        if self.__steps["extractor"] is None:
            raise RuntimeError("No DataExtractor set for this branch")

        self.__steps["extractor"].set_data(source)
        self.__data = self.__steps["extractor"].execute()

        for mapper in self.__steps["mappers"].values():
            mapper.set_data(self.__data)
            self.__data = mapper.execute()

        self.__executed = True
        return self.__data
