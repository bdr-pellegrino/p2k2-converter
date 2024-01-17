from abc import ABC, abstractmethod
from .base_step import BaseStep, T


class DataExtractor(BaseStep, ABC):
    def __init__(self, name: str, source=None):
        super().__init__(name)
        self.__source = source

    def set_data(self, source):
        self.__source = source

    def execute(self) -> T:
        if self.__source is None:
            raise ValueError("No source set for this step")
        return self.extract_data(self.__source)

    @abstractmethod
    def extract_data(self, source) -> T:
        pass



