from p2k2_converter.core.workflow import Workflow


class Gate(Workflow):

    def translation_definition(self, source, model):
        def translation():
            pass

        model.set_translation_strategy(translation)
        return [source, model]
