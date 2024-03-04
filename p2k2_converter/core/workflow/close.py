from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Bar, Cut, Machining
from openpyxl import Workbook
from typing import List
import re


class Close(WorkflowStrategy):

    def __init__(self, row: int, config_file: dict):
        self.__cell_row = row
        self.__profile_config = config_file["CLOSE"]

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

    def cuts_definition(self, workbook, model) -> [Workbook, Model]:
        product_worksheet = workbook[self.__profile_config["worksheet"]]

        for profile in self.__profile_config["profiles"]:
            target_profile = model.profiles[profile["code"]]
            quantity_position = f"{profile['quantity-column']}{self.__cell_row}"
            length_position = f"{profile['length-column']}{self.__cell_row}"

            cut_quantity = product_worksheet[quantity_position].value
            cut_length = product_worksheet[length_position].value

            for _ in range(cut_quantity):
                target_profile.cuts.append(Cut(cut_length, profile["left-angle-cut"], profile["right-angle-cut"]))

            target_profile.length = sum(cut.length for cut in target_profile.cuts)

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
