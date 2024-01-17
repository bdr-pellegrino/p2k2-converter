import unittest
from contextlib import contextmanager

from p2k2_converter.pipeline.source.base_source import BaseSource
from p2k2_converter.pipeline.step.data_extractor import DataExtractor
from p2k2_converter.pipeline.step.data_mapper import DataMapper


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


class DataExtractorTest(unittest.TestCase):

    def setUp(self):
        self.__extractor_no_source = DummyDataExtractor("dummy_extractor")
        self.__extractor_with_source = DummyDataExtractor("dummy_extractor", source=ArraySource())

    def test_cant_extract_if_resource_is_not_set(self):
        with self.assertRaises(ValueError):
            self.__extractor_no_source.execute()

    def test_can_extract_data(self):
        self.assertEqual(self.__extractor_with_source.execute(), [1, 2, 3, 4, 5])

    def test_with_set_data(self):
        self.__extractor_no_source.set_data(ArraySource())
        self.assertEqual(self.__extractor_no_source.execute(), [1, 2, 3, 4, 5])


class DataMapperTest(unittest.TestCase):

    def test_cant_extract_if_resource_is_not_set(self):
        mapper = DummyDataMapper("dummy_mapper")
        with self.assertRaises(ValueError):
            mapper.execute()

    def test_can_extract_data(self):
        extractor = DummyDataExtractor("dummy_extractor", source=ArraySource())
        mapper = DummyDataMapper("mapper", data=extractor.execute())
        self.assertEqual(mapper.execute(), 15)

    def test_with_set_data(self):
        extractor = DummyDataExtractor("dummy_extractor", source=ArraySource())
        mapper = DummyDataMapper("dummy")
        mapper.set_data(extractor.execute())
        self.assertEqual(mapper.execute(), 15)
