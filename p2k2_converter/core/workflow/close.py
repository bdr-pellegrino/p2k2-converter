from typing import List
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.core.classes import Model, Cut, Machining
from p2k2_converter.p2k2 import CutBuilder
from p2k2_converter.core.utils import profile_name, configure_cuts_for_profile
from openpyxl import Workbook
import re


class Close(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "CLOSE")

    def machining_definition(self, workbook, model) -> [Workbook, Model]:
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
            if "machinings" in profile:
                for machining in profile["machinings"]:
                    code = machining["code"]
                    starting_position = f"{machining['starting-column']}{self._cell_row}"
                    ending_position = f"{machining['ending-column']}{self._cell_row}"
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
        info_worksheet = workbook[self._global_config["info-worksheet"]]
        for builder in builders:
            builder.add_label(f"CLOSE ORDER ID {info_worksheet[self._global_config['order-id-position']].value}")
            builder.add_label(f"CLOSE CLIENT ID {info_worksheet[self._global_config['client-id-position']].value}")
            builder.add_label(f"ROW {self._cell_row}")
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
        def translation():
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
                next((profile["height"] for profile in self._model_config["profiles"] if
                      profile["code"] == profile_code), 0)
            )

            door_hole_hinge = [machining for machining in machinings if machining.code == "CERNIERA FORI ANTA"]
            default_offset = 1
            command_verse = next(
                (profile["command-verse"] for profile in self._model_config["profiles"] if
                 profile["code"] == profile_code),
                "DX"
            )

            if command_verse == "DX":
                default_offset = cuts[0].length - default_offset

            builders = configure_cuts_for_profile(builders, door_hole_hinge, height, default_offset)
            builders = self.__apply_labels(builders, workbook)

            frame_cutouts = [machining for machining in machinings if machining.code == "FORO SCASSI TELAIO"]
            builders = configure_cuts_for_profile(builders, frame_cutouts, height, 1)

            output[profile_name(model, profile_code)] = [builder.build() for builder in builders]
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
                output[profile_name(model, profile_code)] = [builder.build() for builder in builders]

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
                output[profile_name(model, profile_code)] = [builder.build() for builder in builders]

            return output

        model.set_translation_strategy(translation)
        return [workbook, model]

