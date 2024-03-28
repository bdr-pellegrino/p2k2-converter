from p2k2_converter.core.workflow import Workflow


class Moderna(Workflow):

    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "MODERNA")

    def translation_definition(self, source, model):
        pass
