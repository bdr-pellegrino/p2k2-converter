from contextlib import contextmanager
from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import BaseStep


class ArraySource(BaseSource):
    @contextmanager
    def open(self):
        yield [1, 2, 3, 4, 5]


class DummyDataExtractor(BaseStep):
    def execute(self, source, data):
        return [source, source]


class DummyDataMapper(BaseStep):
    def execute(self, source, data):
        return [source, sum(data)]


class DoubleMapper(BaseStep):
    def execute(self, source, data):
        doubled_data = [x * 2 for x in data]
        return [source, doubled_data]
