from contextlib import contextmanager
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.utils.exceptions import InvalidFileException
from .base_source import BaseSource


class XlsmSource(BaseSource):

    def __init__(self, path: str):
        super().__init__()
        self.__path = path

    @contextmanager
    def open(self) -> Workbook:
        try:
            wb = load_workbook(self.__path, read_only=True)
            yield wb
            wb.close()
        except FileNotFoundError:
            print(f"Error: File {self.__path} not found.")
            exit(1)
        except InvalidFileException:
            print(f"Error: File {self.__path} is not a valid xlsm file.")
            exit(1)

