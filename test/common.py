from contextlib import contextmanager

from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import DataExtractor
from p2k2_converter.pipeline.step import DataMapper


class ArraySource(BaseSource):
    @contextmanager
    def open(self):
        yield [1, 2, 3, 4, 5]


class DummyDataExtractor(DataExtractor):
    def extract_data(self, source):
        with source.open() as data:
            return data


class DummyDataMapper(DataMapper):
    def extract_data(self, data: list[int]) -> int:
        return sum(data)


class DoubleMapper(DataMapper):
    def extract_data(self, data: list[int]) -> list[int]:
        return [x * 2 for x in data]