from abc import ABC, abstractmethod


class P2k2BuilderInterface(ABC):

    @staticmethod
    @abstractmethod
    def add_version(self, minor: int, major: int) -> 'P2k2BuilderInterface':
        pass

    @staticmethod
    @abstractmethod
    def add_pdat(self, code: str, internal_color_code: str,
                 external_color_code: str, bar_quantity: int) -> 'P2k2BuilderInterface':
        pass

    @staticmethod
    @abstractmethod
    def build(self, p2k2_file_path: str) -> str:
        pass