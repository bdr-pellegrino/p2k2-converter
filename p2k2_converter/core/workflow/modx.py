from abc import ABC
from openpyxl.workbook import Workbook

from p2k2_converter.core.classes import Model
from p2k2_converter.core.workflow import Workflow
from p2k2_converter.p2k2 import CutBuilder
from p2k2_converter.p2k2.translation import Translation


class Modx(Workflow, ABC):

    def translation_definition(self, workbook, model) -> [Workbook, Model]:


        def translation():
            def default_translation(profile, builders, cuts, machinings):
                return tuple([builder.build() for builder in builders])

            def guide_cutting_translation(profile, builders, cuts, machinings):
                model_height = model.height
                profile_code_1 = f"{machinings[0].code} {model_height}"
                profile_code_2 = f"{machinings[1].code} {model_height}"

                builders[0].add_machining(profile_code_1, 1)
                builders[1].add_machining(profile_code_2, 1)

                return tuple([builder.build() for builder in builders])

            order_id, client_id = self.get_product_info(workbook)
            translation_helper = Translation(model, order_id, client_id, self._cell_row)
            translation_helper.add_profile_translation("PROFILO DOGA", default_translation)
            translation_helper.add_profile_translation("TAGLIO GUIDA", guide_cutting_translation)

            return translation_helper.translate()

        model.set_translation_strategy(translation)
        return workbook, model


