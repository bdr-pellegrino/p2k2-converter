from abc import ABC, abstractmethod
from p2k2_converter.p2k2.classes import Cut


class CutBuilder(ABC):

    @staticmethod
    @abstractmethod
    def add_left_cutting_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_right_cutting_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_right_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_left_beta_cutting_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_cut_length(self, length: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_superior_cut_length(self, length: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_inferior_cut_length(self, length: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_left_trim_cut_length(self, length: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_right_trim_cut_length(self, length: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_left_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_right_trim_cut_angle(self, angle: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_order_code(self, code: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_typology(self, typology: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_customer_name(self, name: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_square_number(self, number: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_bar_code(self, code: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_label(self, label: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_machining(self, code: str, offset: int, clamp_near: int = None) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_cut(self, cut: Cut) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_exit(self, exit_number: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_area(self, area: str) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_stop(self, stop_code: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_trolley(self, trolley_code: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_trolley_slot(self, trolley_slot_code: int) -> 'CutBuilder':
        pass

    @staticmethod
    @abstractmethod
    def add_forbidden_space(self, start: int, end: int) -> 'CutBuilder':
        pass

