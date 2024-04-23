from abc import ABC
from p2k2_converter.core.workflow import Workflow


class Full(Workflow, ABC):

    def translation_definition(self, source, model):

        def translate():
            pass

        model.set_translation_strategy(translate)
        return [source, model]

