import unittest
from zipfile import BadZipFile

from p2k2_converter.pipeline.source.xlsm_source import XlsmSource
from openpyxl import Workbook


class XlsmSourceTest(unittest.TestCase):
    def setUp(self):
        """
        Setting up dummy data files
        """
        self.__test_files = {
            "simple": "test/data/dummy.xlsm",
            "malformed": "test/data/dummy.xlsx"
        }

        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"] = "Test"
        workbook.save(self.__test_files["simple"])

        with open(self.__test_files["malformed"], "w") as f:
            f.write("Dummy data")

    def test_open_workbook(self):
        xlsm = XlsmSource(self.__test_files["simple"])
        with xlsm.open() as wb:
            self.assertIsInstance(wb, Workbook)

    def test_open_workbook_that_doesnt_exists(self):
        xlsm = XlsmSource("test/data/doesnt_exists.xlsm")
        with self.assertRaises(FileNotFoundError):
            with xlsm.open() as _:
                pass

    def test_open_malformed_workbook(self):
        xlsm = XlsmSource(self.__test_files["malformed"])
        with self.assertRaises(BadZipFile):
            with xlsm.open() as _:
                pass
