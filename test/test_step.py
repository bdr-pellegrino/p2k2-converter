import unittest
from .common import ArraySource, DummyDataExtractor, DummyDataMapper


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
