from abc import ABC, abstractmethod
from .base_step import BaseStep, T


class DataMapper(BaseStep, ABC):
    def __init__(self, name: str, data: any = None):
        super().__init__(name)
        self.__data = data

    def set_data(self, source):
        self.__data = source

    def execute(self) -> T:
        if self.__data is None:
            raise ValueError("No data provided for this step")
        return self.extract_data(self.__data)

    @abstractmethod
    def extract_data(self, data) -> T:
        pass