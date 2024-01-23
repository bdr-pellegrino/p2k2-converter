from dataclasses import dataclass
from p2k2_converter.core import Machining, Bar
from copy import deepcopy as copy


@dataclass
class Profile:
    code: str
    refinement: float | None
    bars: list[Bar]
    machinings: list[Machining] | None

    def add_machining(self, machining: Machining) -> None:
        self.machinings.append(machining)

    def get_machinings(self) -> list[Machining]:
        return copy(self.machinings)
