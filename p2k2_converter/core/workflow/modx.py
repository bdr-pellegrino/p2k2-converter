from abc import ABC
from openpyxl.workbook import Workbook

from p2k2_converter.core.classes import Model
from p2k2_converter.core.workflow import Workflow


class Modx(Workflow, ABC):

    def translation_definition(self, workbook, model) -> [Workbook, Model]:
        pass
