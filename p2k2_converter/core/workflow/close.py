from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Bar, Cut
from openpyxl import Workbook
from typing import List


class Close(WorkflowStrategy):

    def __init__(self):
        self.__cell_row = None
        self.__profile_config = {
            "PROFILO DOGA": {
                "refinement_position": "CM",
                "quantity_position": "CI",
                "length_position": "CJ",
                "l_angle": 90,
                "r_angle": 90,
                "bar_length": 6000,
                "bar_code": "PROFILO DOGA"
            },
            "CANALINO VERTICALE": {
                "quantity_position": "CR",
                "length_position": "CS",
                "l_angle": 45,
                "r_angle": 45,
                "bar_length": 6000,
                "bar_code": "CANALINO VERTICALE"
            },
            "CANALINO ORIZZONTALE": {
                "quantity_position": "CV",
                "length_position": "CW",
                "l_angle": 45,
                "r_angle": 45,
                "bar_length": 6000,
                "bar_code": "CANALINO ORIZZONTALE"
            },
            "MONTANTE SX": {
                "quantity_position": "DA",
                "length_position": "DB",
                "l_angle": 90,
                "r_angle": 45,
                "bar_length": 6000,
                "bar_code": "MONTANTE SX"
            },
            "TRAVERSO SUPERIORE": {
                "quantity_position": "DE",
                "length_position": "DF",
                "l_angle": 45,
                "r_angle": 90,
                "bar_length": 6000,
                "bar_code": "TRAVERSO SUPERIORE"
            },
            "MONTANTE DX": {
                "quantity_position": "DI",
                "length_position": "DJ",
                "l_angle": 45,
                "r_angle": 45,
                "bar_length": 6000,
                "bar_code": "MONTANTE DX"
            },
            "PROFILO SOGLIA": {
                "quantity_position": "DM",
                "length_position": "DN",
                "l_angle": 90,
                "r_angle": 90,
                "bar_length": 6000,
                "bar_code": "PROFILO SOGLIA"
            }
        }

    def model_definition(self, workbook, data) -> [Workbook, Model]:
        product_worksheet = workbook["prod CLOSE"]
        data_range = product_worksheet["C8:F23"]

        for row in data_range:
            row_cell = [cell.value for cell in row]
            name = row_cell[0]
            if name == "CLOSE":
                self.__cell_row = row[0].row
                width = row_cell[2]
                height = row_cell[3]

                return [workbook, Model(name, width, height)]

    def profiles_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook["prod CLOSE"]

        for profile in self.__profile_config:
            profile_config = self.__profile_config[profile]
            profile_class = Profile(brand="PELLEGRINO", system="CLOSE", code=profile)

            if "refinement_position" in profile_config:
                refinement = product_worksheet[f"{profile_config['refinement_position']}{self.__cell_row}"].value
                if refinement is not None:
                    profile_class.refinement = float(refinement)

            model.profiles[profile] = profile_class

        return [workbook, model]

    def __create_bars(self, cut: Cut, cut_quantity: int, bar_length: float, bar_code: str) -> List[Bar]:
        bars = []
        current_bar = Bar(bar_code, bar_length)

        for _ in range(cut_quantity):
            remaining_length = bar_length - sum(c.length for c in current_bar.cuts)

            if remaining_length < cut.length:
                bars.append(current_bar)
                current_bar = Bar(bar_code, bar_length)

            current_bar.cuts.append(cut)

        if current_bar.cuts:
            bars.append(current_bar)

        return bars

    def __define_bar_cuts(self, worksheet, quantity_position, length_position, l_angle, r_angle, bar_length, bar_code):
        cuts_quantity = worksheet[quantity_position].value
        cut_length = worksheet[length_position].value

        return self.__create_bars(Cut(cut_length, l_angle, r_angle), cuts_quantity, bar_length, bar_code)

    def bars_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook["prod CLOSE"]

        for profile in model.profiles:
            config = self.__profile_config[profile]

            model.profiles[profile].bars = self.__define_bar_cuts(
                product_worksheet,
                f"{config['quantity_position']}{self.__cell_row}",
                f"{config['length_position']}{self.__cell_row}",
                config["l_angle"],
                config["r_angle"],
                config["bar_length"],
                config["bar_code"]
            )

        return [workbook, model]

    def machining_definition(self, workbook, data):
        return f"{workbook} machining definition: {data}"
