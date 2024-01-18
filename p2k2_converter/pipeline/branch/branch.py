from copy import deepcopy as copy
from p2k2_converter.pipeline.step import BaseStep, DataExtractor


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

    def add_step(self, step: BaseStep, force=False) -> None:
        if isinstance(step, DataExtractor):
            if self.__steps["extractor"] is not None and not force:
                raise ValueError("DataExtractor already set for this branch")
            self.__steps["extractor"] = step
        else:
            if step.get_name() in self.__steps["mappers"] and not force:
                raise ValueError("DataMapper already set for this branch")
            self.__steps["mappers"][step.get_name()] = step

    def get_name(self):
        return self.__name

    def get_steps(self):
        return copy(self.__steps)

    def execute(self, source):
        if self.__executed:
            raise RuntimeError("Branch already executed")

        if self.__steps["extractor"] is None:
            raise RuntimeError("No DataExtractor set for this branch")

        self.__steps["extractor"].set_data(source)
        data = self.__steps["extractor"].execute()

        for mapper in self.__steps["mappers"].values():
            mapper.set_data(data)
            data = mapper.execute()

        self.__executed = True

        return data
