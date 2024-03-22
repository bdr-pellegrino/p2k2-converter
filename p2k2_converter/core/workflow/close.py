from typing import List, Dict
from p2k2_converter.core.workflow import WorkflowStrategy
from p2k2_converter.core.classes import Model, Profile, Cut, Machining
from p2k2_converter.p2k2.classes import Machining as P2k2Machining
from p2k2_converter.p2k2 import CutBuilder
from openpyxl import Workbook
import re


def __machining_application_index(dim: int, machinings: List[Machining], offset: int) -> Dict[int, List[Machining]]:
    """
    Calculate how to distribute the profile machinings to the cuts.

    Args:
        dim: The dimension (width or height) of the cut.
        machinings: List of machinings to apply.
        offset: The offset.

    Returns:
        A dictionary where the index refers to the cut index, and the value is a list of machinings
        to apply to the specific cut.
    """
    base = 0
    top = dim
    cut_index = 0

    output = {}
    for machining in sorted(machinings, key=lambda mach: mach.offset):
        while not (base <= machining.offset <= top):
            base = top
            top += dim
            cut_index += 1

        output.setdefault(cut_index, []).append(P2k2Machining(machining.code, offset))

    return output


def configure_cuts_for_profile(builders: List[CutBuilder], machinings: List[Machining], dim: int, offset: int,
                               refinement: int = 0) -> List[CutBuilder]:
    """
    Configure the cuts to add in the profile.

    Args:
        builders: The list of cut builders used to create the cuts
        machinings: The list of machinings to be distributed
        dim: Working dimension
        offset: Offset of the machining
        refinement: The left trim of the bar.

    Returns:
        A list of configured P2k2 cuts
    """
    cut_list = []
    machining_distribution = __machining_application_index(dim, machinings, offset)

    for idx, cut in enumerate(builders):
        if idx in machining_distribution:
            for machining in machining_distribution[idx]:
                cut.add_machining_item(machining)

        if idx == len(builders) - 1 and refinement != 0:
            cut.add_left_trim_cut_length(refinement)

        cut_list.append(cut)

    return cut_list


class Close(WorkflowStrategy):

    def __init__(self, row: int, config_file: dict):
        self.__cell_row = row
        self.__global_config = config_file["GLOBALS"]
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
                    profile_class.refinement = abs(float(refinement))

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
                                   for index, cell in enumerate(hole_position) if index_condition(index) and cell.value]

                    for value in sorted(cell_values):
                        if not value:
                            continue

                        if type(value) == str:
                            match = re.search(r'\b\d+,\d+\b', value)
                            if match:
                                value = float(match.group().replace(',', '.'))

                        model.profiles[profile["code"]].machinings.append(Machining(code, value))

        return [workbook, model]

    def __apply_labels(self, builders: List[CutBuilder], workbook: Workbook):
        """
        Apply the labels to the cuts.

        Args:
            builders: The list of cut builders
            workbook: The workbook instance

        Returns:
            The list of cut builders with the labels applied
        """
        cut_list = []
        info_worksheet = workbook[self.__global_config["info-worksheet"]]
        for builder in builders:
            builder.add_label(f"CLOSE ORDER ID {info_worksheet[self.__global_config['order-id-position']].value}")
            builder.add_label(f"CLOSE CLIENT ID {info_worksheet[self.__global_config['client-id-position']].value}")
            builder.add_label(f"ROW {self.__cell_row}")
            cut_list.append(builder)

        return cut_list

    def translation_definition(self, workbook, model) -> [Workbook, Model]:
        """
        Define the conversion of the Model in a P2K2 class.
        Here are defined the profiles that are used in the production of a close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """

        def translation(inner_self):
            output = {}

            # Handling "PROFILO DOGA" profile
            profile_code = "PROFILO DOGA"
            profile = model.profiles[profile_code]
            cuts = profile.cuts

            # Create a list of CutBuilder with the information of the cuts
            builders = [
                CutBuilder().add_cut_length(cut.length)
                .add_left_cutting_angle(cut.angleL)
                .add_right_cutting_angle(cut.angleR)
                for cut in cuts
            ]
            machinings = profile.machinings

            height = int(
                next((profile["height"] for profile in self.__model_config["profiles"] if
                      profile["code"] == profile_code), 0)
            )

            door_hole_hinge = [machining for machining in machinings if machining.code == "CERNIERA FORI ANTA"]
            default_offset = 1
            command_verse = next(
                (profile["command-verse"] for profile in self.__model_config["profiles"] if
                 profile["code"] == profile_code),
                "DX"
            )

            if command_verse == "DX":
                default_offset = cuts[0].length - default_offset

            builders = configure_cuts_for_profile(builders, door_hole_hinge, height, default_offset)
            builders = self.__apply_labels(builders, workbook)

            frame_cutouts = [machining for machining in machinings if machining.code == "FORO SCASSI TELAIO"]
            builders = configure_cuts_for_profile(builders, frame_cutouts, height, 1)

            output[profile_code] = [builder.build() for builder in builders]
            # Handling "MONTANTE SX" and MONTANTE DX profile
            profile_codes = ["MONTANTE SX", "MONTANTE DX"]
            for profile_code in profile_codes:

                profile = model.profiles[profile_code]
                cuts = profile.cuts
                default_offset = 1
                builders = [
                    CutBuilder().add_cut_length(cut.length)
                    .add_left_cutting_angle(cut.angleL)
                    .add_right_cutting_angle(cut.angleR)
                    for cut in cuts
                ]

                builders = configure_cuts_for_profile(builders, profile.machinings, profile.length, default_offset)
                builders = self.__apply_labels(builders, workbook)
                output[profile_code] = [builder.build() for builder in builders]

            # Handling profiles without machinings
            profile_codes = ["CANALINO VERTICALE", "CANALINO ORIZZONTALE", "TRAVERSO SUPERIORE", "PROFILO SOGLIA"]
            for profile_code in profile_codes:
                profile = model.profiles[profile_code]
                cuts = profile.cuts
                builders = [
                    CutBuilder().add_cut_length(cut.length)
                    .add_left_cutting_angle(cut.angleL)
                    .add_right_cutting_angle(cut.angleR)
                    for cut in cuts
                ]
                builders = self.__apply_labels(builders, workbook)
                output[profile_code] = [builder.build() for builder in builders]

            return output

        model.set_translation_strategy(translation)
        return [workbook, model]

