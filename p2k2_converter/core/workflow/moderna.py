from p2k2_converter.core.classes import Model
from p2k2_converter.core.workflow import WorkflowStrategy


class Moderna(WorkflowStrategy):

    def __init__(self, row: int, config_file: dict):
        self.__cell_row = row
        self.__global_config = config_file["GLOBALS"]
        self.__model_config = config_file["MODERNA"]

    def model_definition(self, workbook, data):

        product_worksheet = workbook[self.__model_config["worksheet"]]

        data_row = product_worksheet[
            f"{self.__model_config['product-column']}{self.__cell_row}:{self.__model_config['height-column']}{self.__cell_row}"
        ]
        cell_data = [cell.value for row in data_row for cell in row]

        name = cell_data[0]
        width = cell_data[2]
        height = cell_data[3]
        return [workbook, Model(name, width, height)]

        pass

    def profiles_definition(self, source, model):
        pass

    def cuts_definition(self, source, model):
        pass

    def machining_definition(self, source, model):
        pass

    def translation_definition(self, source, model):
        pass
