from p2k2_converter.core.workflow import Modx


class Modi(Modx):
    def __init__(self, row: int, config_file: dict):
        super().__init__(row, config_file, "MODI")
