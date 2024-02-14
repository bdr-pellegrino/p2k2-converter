import unittest
from test.data import INPUT_FILE
from p2k2_converter.core import Parser
from p2k2_converter.config import DEFAULT_CONFIG
from p2k2_converter.p2k2 import Translator


class TranslatorTest(unittest.TestCase):

    def setUp(self):

        parser = Parser(workbook_path=INPUT_FILE, config_file=DEFAULT_CONFIG)
        self.__order = parser.parse()
        self.__translator = Translator()

    def test_translate(self):
        job = self.__translator.p2k2_translation(self.__order)
        print(job)
