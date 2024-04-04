from p2k2_converter.core.classes import Profile
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder


class Moderna(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "MODERNA")

    def translation_definition(self, workbook, model):

        def translation():
            output = {}

            # Handling "PROFILO DOGA" profile
            profile_code = "PROFILO DOGA"
            profile = model.profiles[profile_code]
            cuts = profile.cuts
            machinings = profile.machinings

            builders = [
                CutBuilder().add_cut_length(cut.length)
                .add_left_cutting_angle(cut.angleL)
                .add_right_cutting_angle(cut.angleR)
                for cut in cuts
            ]

            cut_len = cuts[0].length
            working_code = machinings[0].code
            builders[0].add_machining(working_code, machinings[0].offset) \
                .add_machining(working_code, cut_len - machinings[1].offset)
            builders[-1].add_machining(working_code, machinings[2].offset) \
                .add_machining(working_code, cut_len - machinings[3].offset)

            builders = self.apply_labels(builders, workbook)
            output[profile_code] = [builder.build() for builder in builders]

            # Handling "PROFILO GANCIO-UNCINO" profile
            profile_code = "PROFILO GANCIO-UNCINO"
            profile = model.profiles[profile_code]
            cuts = profile.cuts

            builders = [
                CutBuilder().add_cut_length(cut.length)
                .add_left_cutting_angle(cut.angleL)
                .add_right_cutting_angle(cut.angleR)
                for cut in cuts
            ]
            builders = self.apply_labels(builders, workbook)
            output[profile_code] = [builder.build() for builder in builders]

            # Handling "CERNIERA TUBOLARE", "CERNIERA APERTA" and "H" profiles
            profile_codes = ["CERNIERA TUBOLARE", "CERNIERA APERTA", "H"]
            for profile_code in profile_codes:
                if profile_code not in model.profiles:
                    continue

                profile = model.profiles[profile_code]
                cuts = profile.cuts
                builders = [
                    CutBuilder().add_cut_length(cut.length)
                    .add_left_cutting_angle(cut.angleL)
                    .add_right_cutting_angle(cut.angleR)
                    for cut in cuts
                ]
                builders = self.apply_labels(builders, workbook)
                output[profile_code] = [builder.build() for builder in builders]

            return output

        model.set_translation_strategy(translation)
        return [workbook, model]


