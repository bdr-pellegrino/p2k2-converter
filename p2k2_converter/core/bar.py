from dataclasses import dataclass
from p2k2_converter.core import Cut
from copy import deepcopy as copy


@dataclass
class Bar:
    name: str
    length: float
    cuts: list[Cut]

    def add_cut(self, cut: Cut) -> None:
        self.cuts.append(cut)

    def get_cuts(self) -> list[Cut]:
        return copy(self.cuts)
