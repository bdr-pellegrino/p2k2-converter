from p2k2_converter.core.utils import configure_cuts_for_profile
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder


class ClickRapid(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "CLICK_RAPID")

    def translation_definition(self, workbook, model):
        """
        Define the conversion of the Model in a P2K2 class.
        Here are defined the profiles that are used in the production of a close product.

        Args:
            workbook: An open Workbook instance use for extracting the data.
            model: The model created in the model_definition step

        Returns:
            A tuple containing the Workbook and the created model. These object will be used in the next steps
        """

        product_worksheet = workbook[self._model_config["worksheet"]]
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

            builders[0].add_machining(machinings[0].code, 1)
            last_cut = builders[-1] if len(cuts) > 1 else builders[0]
            last_cut.add_machining(machinings[1].code, 1)

            offset = 0
            for i in range(2, len(machinings)):
                last_cut.add_machining(machinings[i].code, offset + machinings[i].offset)
                offset += machinings[i].offset

            builders = self.apply_labels(builders, workbook)
            output[profile_code] = [builder.build() for builder in builders]

            profile_codes = ["CANALINO VERTICALE", "PROFILO DI TENUTA LATERALE"]
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

