from contextlib import contextmanager
from openpyxl import load_workbook
from openpyxl.workbook import Workbook

from p2k2_converter.source.source import Source


class XlsmSource(Source):
    def __init__(self, path):
        super().__init__()
        self.__path = path

    @contextmanager
    def open(self) -> Workbook:
        wb = load_workbook(self.__path, read_only=True)
        yield wb
        wb.close()
