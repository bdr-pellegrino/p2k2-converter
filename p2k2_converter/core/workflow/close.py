from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model


class Close(WorkflowStrategy):
    def model_definition(self, source, data):
        workbook = source
        data_insertion_worksheet = workbook["IMMISSIONE DATI"]
        data_range = data_insertion_worksheet["I64:L79"]

        for row in data_range:
            row_cell = [cell.value for cell in row]
            name = row_cell[0]
            if name == "CLOSE":
                width = row_cell[2]
                height = row_cell[3]
                return Model(name, width, height)

    def profiles_definition(self, source, data):
        return f"{source} profiles definition: {data}"

    def bars_definition(self, source, data):
        return f"{source} bars definition: {data}"

    def machining_definition(self, source, data):
        return f"{source} machining definition: {data}"
