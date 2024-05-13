from p2k2_converter.core.utils import configure_cuts_for_profile
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder
from p2k2_converter.p2k2.translation import Translation


class Gate(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "GATE")

    def translation_definition(self, workbook, model):

        def stave_profile_translation(profile, builders, cuts, machinings):
            code = "PROFILO DOGA"
            height = int(
                next((profile["height"] for profile in self._model_config["profiles"] if profile["code"] == code), 0)
            )

            door_hole_hinge = [machining for machining in machinings if machining.code == "CERNIERA FORI ANTA"]
            default_offset = 1
            command_verse = next(
                (profile["command-verse"] for profile in self._model_config["profiles"] if
                 profile["code"] == code),
                "DX"
            )

            if command_verse == "DX":
                default_offset = cuts[0].length - default_offset

            builders = configure_cuts_for_profile(builders, door_hole_hinge, height, default_offset)

            frame_cutouts = [machining for machining in machinings if machining.code == "FORO SCASSI TELAIO"]
            builders = configure_cuts_for_profile(builders, frame_cutouts, height, 1)

            return tuple([builder.build() for builder in builders])

        def pillar_translation(profile, builders, cuts, machinings):
            default_offset = 1
            builders = configure_cuts_for_profile(builders, profile.machinings, profile.length, default_offset)
            return tuple([builder.build() for builder in builders])

        def default_translation(profile, builders, cuts, machinings):
            return tuple([builder.build() for builder in builders])

        def translation():

            order_id, client_id = self.get_product_info(workbook)
            translation_helper = Translation(model, order_id, client_id, self._cell_row)
            translation_helper.add_profile_translation("PROFILO DOGA", stave_profile_translation)

            profile_codes = ["MONTANTE SX", "MONTANTE DX"]
            for profile_code in profile_codes:
                translation_helper.add_profile_translation(profile_code, pillar_translation)

            profile_codes = ["CANALINO VERTICALE", "CANALINO ORIZZONTALE", "TRAVERSO SUPERIORE", "PROFILO SOGLIA"]
            for profile_code in profile_codes:
                translation_helper.add_profile_translation(profile_code, default_translation)

            return translation_helper.translate()

        model.set_translation_strategy(translation)
        return [workbook, model]
