import unittest
from p2k2_converter.source.xlsm_source import XlsmSource
from openpyxl import Workbook

class XlsmSourceTest(unittest.TestCase):
    def setUp(self):
        """
        Setting up dummy data files
        """
        self.__test_files = {
            "simple": "test/data/dummy.xlsm"
        }

        workbook = Workbook()
        sheet = workbook.active
        sheet["A1"] = "Test"
        workbook.save(self.__test_files["simple"])

    def test_open_workbook(self):
        xlsm = XlsmSource(self.__test_files["simple"])
        with xlsm.open() as wb:
            self.assertIsInstance(wb, Workbook)
