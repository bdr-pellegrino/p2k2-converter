from p2k2_converter.core.classes import Profile
from p2k2_converter.core.utils import configure_cuts_for_profile
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder
from p2k2_converter.p2k2.translation import Translation


class Moderna(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "MODERNA")

    def translation_definition(self, workbook, model):

        def stave_profile_translation(profile, builders, cuts, machinings):
            cut_len = cuts[0].length
            working_code = machinings[0].code
            builders[0].add_machining(working_code, machinings[0].offset) \
                .add_machining(working_code, cut_len - machinings[1].offset)
            builders[-1].add_machining(working_code, machinings[2].offset) \
                .add_machining(working_code, cut_len - machinings[3].offset)

            return tuple([builder.build() for builder in builders])

        def configuration_cut_translation(profile, builders, cuts, machinings):
            default_offset = 1
            builders = configure_cuts_for_profile(builders, profile.machinings, profile.length, default_offset)
            return tuple([builder.build() for builder in builders])

        def default_translation(profile, builders, cuts, machinings):
            return tuple([builder.build() for builder in builders])

        def translation():
            order_id, client_id = self.get_product_info(workbook)
            translation_helper = Translation(model, order_id, client_id, self._cell_row)
            translation_helper.add_profile_translation("PROFILO DOGA", stave_profile_translation)
            translation_helper.add_profile_translation("PROFILO GANCIO-UNCINO", default_translation)

            profile_codes = ["CERNIERA TUBOLARE", "CERNIERA APERTA", "H"]
            for profile_code in profile_codes:
                if profile_code not in model.profiles:
                    continue
                translation_helper.add_profile_translation(profile_code, configuration_cut_translation)

            return translation_helper.translate()

        model.set_translation_strategy(translation)
        return [workbook, model]


