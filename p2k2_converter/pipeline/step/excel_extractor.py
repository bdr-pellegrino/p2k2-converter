from openpyxl.workbook import Workbook
from p2k2_converter.pipeline.step import BaseStep
from p2k2_converter.pipeline.step.base_step import T, Q


class ExcelExtractor(BaseStep):
    def execute(self, source: Workbook, data: any) -> list[T, Q]:
        pass
