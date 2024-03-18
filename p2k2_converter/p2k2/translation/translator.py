from typing import List
from p2k2_converter.p2k2.classes import Bar
import yaml


class Translator:

    def __init__(self, config_file: str):
        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def p2k2_translation(self, order):
        pass

    def __define_bars(self, profile, default_bar_length: int) -> List[Bar]:
        pass
