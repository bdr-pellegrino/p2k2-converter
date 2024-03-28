from abc import ABC
from p2k2_converter.core.classes import Model, Profile, Cut
from p2k2_converter.core.workflow import WorkflowStrategy


class Workflow(WorkflowStrategy, ABC):

    def __init__(self, row: int, config_file: dict, product_name: str):
        self._cell_row = row
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
        pass

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

