import unittest
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


class DataExtractorTest(unittest.TestCase):

    def setUp(self):
        self.__extractors = {
            "no_source": DummyDataExtractor("dummy_extractor"),
            "with_source": DummyDataExtractor("dummy_extractor", source=ArraySource())
        }

    def test_cant_extract_if_resource_is_not_set(self):
        with self.assertRaises(ValueError):
            self.__extractors["no_source"].execute()

    def test_can_extract_data(self):
        self.assertEqual(self.__extractors["with_source"].execute(), [1, 2, 3, 4, 5])

    def test_with_set_data(self):
        self.__extractors["no_source"].set_data(ArraySource())
        self.assertEqual(self.__extractors["no_source"].execute(), [1, 2, 3, 4, 5])


class DataMapperTest(unittest.TestCase):

    def setUp(self):
        self.__extractor = DummyDataExtractor("dummy_extractor", source=ArraySource())

        self.__mappers = {
            "no_data": DummyDataMapper("dummy_mapper"),
            "with_data": DummyDataMapper("dummy_mapper", data=self.__extractor.execute())
        }

    def test_cant_extract_if_resource_is_not_set(self):
        with self.assertRaises(ValueError):
            self.__mappers["no_data"].execute()

    def test_can_extract_data(self):
        self.assertEqual(self.__mappers["with_data"].execute(), 15)

    def test_with_set_data(self):
        self.__mappers["no_data"].set_data(self.__extractor.execute())
        self.assertEqual(self.__mappers["no_data"].execute(), 15)
