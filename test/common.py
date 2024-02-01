from contextlib import contextmanager

from typing_extensions import override

from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import DataExtractor, BaseStep
from p2k2_converter.pipeline.step import DataMapper


class ArraySource(BaseSource):
    @contextmanager
    def open(self):
        yield [1, 2, 3, 4, 5]


class DummyDataExtractor(BaseStep):
    def execute(self, source, data):
        with source.open() as opened_data:
            return [source, opened_data]


class DummyDataMapper(BaseStep):
    def execute(self, source, data):
        return [source, sum(data)]


class DoubleMapper(BaseStep):
    def execute(self, source, data):
        doubled_data = [x * 2 for x in data]
        return [source, doubled_data]
