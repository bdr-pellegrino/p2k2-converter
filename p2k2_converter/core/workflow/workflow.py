from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Bar, Cut, Machining
from openpyxl import Workbook
from typing import List
import re


class Workflow(WorkflowStrategy):

    def __init__(self, row: int, config_file: dict, workflow_name: str):
        self.__cell_row = row
        self.__profile_config = config_file[workflow_name]

    def model_definition(self, workbook, data) -> [Workbook, Model]:
        product_worksheet = workbook[self.__profile_config["worksheet"]]
        data_row = product_worksheet[
            f"{self.__profile_config['product-column']}{self.__cell_row}:{self.__profile_config['height-column']}{self.__cell_row}"
        ]
        cell_data = [cell.value for row in data_row for cell in row]

        name = cell_data[0]
        width = cell_data[2]
        height = cell_data[3]
        return [workbook, Model(name, width, height)]

    def profiles_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook[self.__profile_config["worksheet"]]

        for profile in self.__profile_config["profiles"]:
            profile_class = Profile(brand=profile["brand"], system=profile["system"], code=profile["code"])

            if "refinement-column" in profile:
                refinement = product_worksheet[f"{profile['refinement-column']}{self.__cell_row}"].value
                if refinement is not None:
                    profile_class.refinement = float(refinement)

            model.profiles[profile["code"]] = profile_class

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
        product_worksheet = workbook[self.__profile_config["worksheet"]]

        for profile in self.__profile_config["profiles"]:
            target_profile = model.profiles[profile["code"]]
            target_profile.bars = self.__define_bar_cuts(
                product_worksheet,
                f"{profile['quantity-column']}{self.__cell_row}",
                f"{profile['length-column']}{self.__cell_row}",
                profile["left-angle-cut"],
                profile["right-angle-cut"],
                profile["bar-length"],
                profile["bar-code"]
            )

            target_profile.length = sum(cut.length for bar in target_profile.bars for cut in bar.cuts)

        return [workbook, model]

    def machining_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook[self.__profile_config["worksheet"]]

        for profile in self.__profile_config["profiles"]:

            if "machinings" in profile:
                for machining in profile["machinings"]:

                    starting_position = f"{machining['starting-column']}{self.__cell_row}"
                    ending_position = f"{machining['ending-column']}{self.__cell_row}"
                    cell_data = product_worksheet[f"{starting_position}:{ending_position}"]

                    cell_values = [cell.value for hole_position in cell_data for cell in hole_position]
                    for value in cell_values:
                        # Sanitize the value transforming it to a float
                        if type(value) == str:
                            match = re.search(r'\b\d+,\d+\b', value)
                            if match:
                                value = float(match.group().replace(',', '.'))

                        model.profiles[profile["code"]].machinings.append(Machining(machining["code"], value))

        return [workbook, model]
