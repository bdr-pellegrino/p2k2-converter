from typing import List, Dict
from types import MethodType

from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Cut, Machining
from p2k2_converter.p2k2.classes import Machining as P2k2Machining
from openpyxl import Workbook
import re

from p2k2_converter.p2k2 import CutBuilder


def machining_application_index(dim: int, machinings: List[Machining], offset: int) -> Dict[int, List[Machining]]:
    """
    Calculate how distribute the profile Machinings to the cuts

    Args:
        dim: The dimension (width or height) of the cut
        machinings: List of machinings to apply
        offset: The offset

    Returns:
        A dictionary in which the index is referred to the cut index and the value is a List of Machining to apply
        to the specific cut
    """
    base = 0
    top = dim
    cut_index = 0

    output = dict()

    for machining in sorted(machinings, key=lambda mach: mach.offset):

        while not (base <= machining.offset <= top):
            base = top
            top = top + dim
            cut_index += 1

        if cut_index not in output:
            output[cut_index] = []
        output[cut_index].append(P2k2Machining(machining.code, offset))

    return output


class Close(WorkflowStrategy):

    def __init__(self, row: int, config_file: dict):
        self.__cell_row = row
        self.__model_config = config_file["CLOSE"]

    def model_definition(self, workbook, data) -> [Workbook, Model]:
        """
        Configure a Close model.
        Information relative to name, width and height are extracted and a Model class is created.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            data: An initial preconfigured data used for adding more information.

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self.__model_config["worksheet"]]

        data_row = product_worksheet[
            f"{self.__model_config['product-column']}{self.__cell_row}:{self.__model_config['height-column']}{self.__cell_row}"
        ]
        cell_data = [cell.value for row in data_row for cell in row]

        name = cell_data[0]
        width = cell_data[2]
        height = cell_data[3]
        return [workbook, Model(name, width, height)]

    def profiles_definition(self, workbook, model) -> [Workbook, Model]:
        """
        Configure and add the profiles to the Close model.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step.

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self.__model_config["worksheet"]]

        for profile in self.__model_config["profiles"]:
            profile_class = Profile(brand=profile["brand"], system=profile["system"], code=profile["code"])

            if "refinement-column" in profile:
                refinement = product_worksheet[f"{profile['refinement-column']}{self.__cell_row}"].value
                if refinement is not None:
                    profile_class.refinement = float(refinement)

            model.profiles[profile["code"]] = profile_class

        return [workbook, model]

    def cuts_definition(self, workbook, model) -> [Workbook, Model]:
        """
        Configure and add the cuts to be applied to the Close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self.__model_config["worksheet"]]

        for profile in self.__model_config["profiles"]:
            target_profile = model.profiles[profile["code"]]
            quantity_position = f"{profile['quantity-column']}{self.__cell_row}"
            length_position = f"{profile['length-column']}{self.__cell_row}"

            cut_quantity = product_worksheet[quantity_position].value
            cut_length = product_worksheet[length_position].value
            cut_height = profile["height"]

            for _ in range(cut_quantity):
                target_profile.cuts.append(
                    Cut(cut_length, cut_height, profile["left-angle-cut"], profile["right-angle-cut"])
                )

            target_profile.length = sum(cut.length for cut in target_profile.cuts)
        return [workbook, model]

    def machining_definition(self, workbook, model) -> [Workbook, Model]:
        """
        Configure and add the cuts to be applied to the Close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self.__model_config["worksheet"]]

        for profile in self.__model_config["profiles"]:
            if "machinings" in profile:
                for machining in profile["machinings"]:
                    code = machining["code"]
                    starting_position = f"{machining['starting-column']}{self.__cell_row}"
                    ending_position = f"{machining['ending-column']}{self.__cell_row}"
                    cell_data = product_worksheet[f"{starting_position}:{ending_position}"]

                    index_condition = lambda index: index % 2 == 0 if code == "CERNIERA FORI ANTA" else True
                    cell_values = [cell.value for hole_position in cell_data
                                   for index, cell in enumerate(hole_position) if index_condition(index)]

                    for value in sorted(cell_values):
                        if type(value) == str:
                            match = re.search(r'\b\d+,\d+\b', value)
                            if match:
                                value = float(match.group().replace(',', '.'))
                        model.profiles[profile["code"]].machinings.append(Machining(code, value))

        return [workbook, model]

    def translation_definition(self, workbook, model) -> [Workbook, Model]:
        def translation(inner_self):
            cut_list = []

            for profile_code in model.profiles:
                profile = model.profiles[profile_code]
                cuts = profile.cuts

                height = int(
                    next((profile["height"] for profile in self.__model_config["profiles"] if
                          profile["code"] == profile_code), 0)
                )

                machining_distribution = machining_application_index(height, profile.machinings, 1)

                for idx, cut in enumerate(cuts):
                    cut_builder = CutBuilder()
                    cut_builder.add_cut_length(cut.length)
                    cut_builder.add_left_cutting_angle(cut.angleL)
                    cut_builder.add_right_cutting_angle(cut.angleR)

                    if idx in machining_distribution:
                        for machining in machining_distribution[idx]:
                            cut_builder.add_machining_item(machining)

                    cut_list.append(cut_builder.build())

                return cut_list

        model.translate = MethodType(translation, model)
        return [workbook, model]
