from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2.translation import Translation


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
        def stave_profile_translation(profile, builders, cuts, machinings):
            builders[0].add_machining(machinings[0].code, 1)
            last_cut = builders[-1] if len(cuts) > 1 else builders[0]
            last_cut.add_machining(machinings[1].code, 1)

            offset = 0
            for i in range(2, len(machinings)):
                last_cut.add_machining(machinings[i].code, offset + machinings[i].offset)
                offset += machinings[i].offset

            return tuple([builder.build() for builder in builders])

        def default_translation(profile, builders, cuts, machinings):
            return tuple([builder.build() for builder in builders])

        def translation():
            order_id, client_id = self.get_product_info(workbook)
            translation_helper = Translation(model, order_id, client_id, self._cell_row)
            translation_helper.add_profile_translation("PROFILO DOGA", stave_profile_translation)

            profile_codes = ["CANALINO VERTICALE", "PROFILO DI TENUTA LATERALE"]
            for profile_code in profile_codes:
                if profile_code not in model.profiles:
                    continue

                translation_helper.add_profile_translation(profile_code, default_translation)

            return translation_helper.translate()

        model.set_translation_strategy(translation)
        return [workbook, model]

