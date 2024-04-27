from abc import ABC
from openpyxl.workbook import Workbook

from p2k2_converter.core.classes import Model
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder


class Modx(Workflow, ABC):

    def translation_definition(self, workbook, model) -> [Workbook, Model]:
        def translation():
            output = {}

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

            builders = self.apply_labels(builders, workbook)
            output[profile_code] = [builder.build() for builder in builders]

            profile_code = "TAGLIO GUIDA"
            profile = model.profiles[profile_code]
            cuts = profile.cuts
            machinings = profile.machinings

            model_height = model.height
            profile_code_1 = f"{machinings[0].code} {model_height}"
            profile_code_2 = f"{machinings[1].code} {model_height}"

            builders = [
                CutBuilder().add_cut_length(cut.length)
                .add_left_cutting_angle(cut.angleL)
                .add_right_cutting_angle(cut.angleR)
                for cut in cuts
            ]

            builders[0].add_machining(profile_code_1, 1)
            builders[1].add_machining(profile_code_2, 1)

            output[profile_code] = [builder.build() for builder in builders]

            return output

        model.set_translation_strategy(translation)
        return workbook, model


