from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile
from openpyxl import Workbook


class Close(WorkflowStrategy):
    def model_definition(self, workbook, data) -> [Workbook, Model]:
        data_insertion_worksheet = workbook["IMMISSIONE DATI"]
        data_range = data_insertion_worksheet["I64:L79"]

        for row in data_range:
            row_cell = [cell.value for cell in row]
            name = row_cell[0]
            if name == "CLOSE":
                width = row_cell[2]
                height = row_cell[3]
                return [workbook, Model(name, width, height)]

    def profiles_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook["prod CLOSE"]
        # "Profilo doga"
        stave_profile = Profile(brand="PELLEGRINO", system="CLOSE", code="PROFILO DOGA")
        refinement = product_worksheet["CM8"].value

        if refinement is not None:
            stave_profile.refinement = float(refinement)
        model.profiles.append(stave_profile)

        # "Canalino verticale"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="CANALINO VERTICALE"))

        # "Canalino orizzontale"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="CANALINO ORIZZONTALE"))

        # "Telaio ad elle"
        # 1.0 "Montante Sx"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="MONTANTE SX"))

        # 2.0 "Traverso superiore"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="TRAVERSO SUPERIORE"))

        # 3.0 "Montante Dx"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="MONTANTE DX"))

        # "Profilo soglia"
        model.profiles.append(Profile(brand="PELLEGRINO", system="CLOSE", code="PROFILO SOGLIA"))

        return [workbook, model]


    def bars_definition(self, workbook, data):
        return f"{workbook} bars definition: {data}"

    def machining_definition(self, workbook, data):
        return f"{workbook} machining definition: {data}"
