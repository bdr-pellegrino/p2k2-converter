from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Cut, Machining
from openpyxl import Workbook


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
                    Cut(cut_length, cut_height, profile["left-angle-cut"], profile["right-angle-cut"]))

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
        for profile in self.__model_config["profiles"]:
            if "machinings" in profile:
                for machining in profile["machinings"]:
                    offset = 1  # TODO: define the correct offset
                    model.profiles[profile["code"]] \
                        .machinings \
                        .append(Machining(machining["code"], offset, machining["verse"]))

        return [workbook, model]
