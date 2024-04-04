from abc import ABC
from typing import List
from p2k2_converter.p2k2 import CutBuilder
from openpyxl.workbook import Workbook
from p2k2_converter.core.classes import Model, Profile, Cut, Machining
from p2k2_converter.core.workflow import WorkflowStrategy
import re
import logging


class Workflow(WorkflowStrategy, ABC):

    def __init__(self, row: int, config_file: dict, product_name: str):
        self._cell_row = row
        self._product_name = product_name
        self._global_config = config_file["GLOBALS"]
        self._model_config = config_file[product_name]

    def model_definition(self, workbook, data):
        """
        Configure the model to be produced.
        Information relative to name, width and height are extracted and a Model class is created.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            data: An initial preconfigured data used for adding more information.

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self._model_config["worksheet"]]

        data_row = product_worksheet[
            f"{self._model_config['product-column']}{self._cell_row}:{self._model_config['height-column']}{self._cell_row}"
        ]
        cell_data = [cell.value for row in data_row for cell in row]

        name = cell_data[0]
        width = cell_data[2]
        height = cell_data[3]
        return [workbook, Model(name, width, height)]

    def profiles_definition(self, workbook, model):
        """
        Configure and add the profiles to the model.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step.

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self._model_config["worksheet"]]

        for profile in self._model_config["profiles"]:
            if "in-stock-column" in profile:
                in_stock = product_worksheet[f"{profile['in-stock-column']}{self._cell_row}"].value
                if in_stock is not None:
                    continue

            profile_class = Profile(brand=profile["brand"], system=profile["system"], code=profile["code"])

            if "refinement-column" in profile:
                refinement = product_worksheet[f"{profile['refinement-column']}{self._cell_row}"].value
                if refinement is not None:
                    profile_class.refinement = abs(float(refinement))

            model.profiles[profile["code"]] = profile_class

        return [workbook, model]

    def cuts_definition(self, workbook, model):
        """
        Configure and add the cuts to be applied to the Close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self._model_config["worksheet"]]

        for profile in self._model_config["profiles"]:
            if profile["code"] not in model.profiles:
                continue

            target_profile = model.profiles[profile["code"]]
            quantity_position = f"{profile['quantity-column']}{self._cell_row}"
            length_position = f"{profile['length-column']}{self._cell_row}"

            cut_quantity = product_worksheet[quantity_position].value

            cut_length = product_worksheet[length_position].value
            cut_height = profile["height"]

            for _ in range(cut_quantity):
                target_profile.cuts.append(
                    Cut(cut_length, cut_height, profile["left-angle-cut"], profile["right-angle-cut"])
                )

            target_profile.length = sum(cut.length for cut in target_profile.cuts)
        return [workbook, model]

    def get_machinings_for_profile(self, product_worksheet, profile, filter_index=None):
        """
        Return the list of the machining for a profile
        Args:
            product_worksheet: The worksheet with the information to gather.
            profile: The profile associated to the machings.
            filter_index: a function for filtering the values of the machinings.

        Returns:
            A list of Machining class
        """

        output = []
        if "machinings" in profile:
            for machining in profile["machinings"]:
                code = machining["code"]
                if 'starting-column' and 'ending-column' in machining:
                    starting_position = f"{machining['starting-column']}{self._cell_row}"
                    ending_position = f"{machining['ending-column']}{self._cell_row}"
                    cell_data = product_worksheet[f"{starting_position}:{ending_position}"]

                    cell_values = [
                       cell.value for position in cell_data
                       for index, cell in enumerate(position)
                       if filter_index(index, code) and cell.value
                    ]

                    for value in sorted(cell_values):
                        if not value:
                            continue

                        if type(value) == str:
                            match = re.search(r'\b\d+,\d+\b', value)
                            if match:
                                value = float(match.group().replace(',', '.'))
                        output.append(Machining(code, value))
                else:
                    message = f"Configuration for {code} machining doesn't comprehend starting and ending position"
                    logging.warning(message)
                    output.append(Machining(code, 0))

        return output

    def machining_definition(self, workbook, model):
        """
        Configure and add the cuts to be applied to the Close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """
        product_worksheet = workbook[self._model_config["worksheet"]]
        for profile in self._model_config["profiles"]:
            if profile["code"] not in model.profiles:
                continue
            machining_list = self.get_machinings_for_profile(product_worksheet, profile)
            for machining in machining_list:
                model.profiles[profile["code"]].machinings.append(machining)
        return [workbook, model]

    def apply_labels(self, builders: List[CutBuilder], workbook: Workbook):
        """
        Apply the labels to the cuts.

        Args:
            builders: The list of cut builders
            workbook: The workbook instance

        Returns:
            The list of cut builders with the labels applied
        """
        cut_list = []
        info_worksheet = workbook[self._global_config["info-worksheet"]]
        for builder in builders:
            builder.add_label(f"{self._product_name} ORDER ID {info_worksheet[self._global_config['order-id-position']].value}")
            builder.add_label(f"{self._product_name} CLIENT ID {info_worksheet[self._global_config['client-id-position']].value}")
            builder.add_label(f"ROW {self._cell_row}")
            cut_list.append(builder)

        return cut_list
