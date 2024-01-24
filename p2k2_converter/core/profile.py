from dataclasses import dataclass
from p2k2_converter.core import Machining, Bar


@dataclass
class Profile:
    code: str
    refinement: float | None
    bars: dict[str, Bar]
    machinings: dict[str, Machining]

    def add_bar(self, bar: Bar) -> None:
        self.bars[bar.code] = bar

    def remove_bar(self, code: str) -> None:
        del self.bars[code]

    def get_bars(self) -> list[Bar]:
        return list(self.bars.values())

    def add_machining(self, machining: Machining) -> None:
        self.machinings[machining.code] = machining

    def remove_machining(self, code: str) -> None:
        del self.machinings[code]

    def get_machinings(self) -> list[Machining]:
        return list(self.machinings.values())

