from abc import ABC, abstractmethod
from p2k2_converter.p2k2.classes import Cut


class BarBuilder(ABC):

    def __init__(self, brand: str, system: str, profile_code: str):
        self._brand = brand
        self._system = system
        self._profile_code = profile_code

    @staticmethod
    @abstractmethod
    def add_inner_color(self, inner_color: str) -> 'BarBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_outer_color(self, outer_color: str) -> 'BarBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_length(self, length: float) -> 'BarBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_remaining_length(self, remaining_length: float) -> 'BarBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_cut(self, cut: Cut) -> 'BarBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_sfrido(self, code: str, trolley: int, slot: int) -> 'BarBuilder':
        pass


