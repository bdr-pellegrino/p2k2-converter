from dataclasses import dataclass
from p2k2_converter.core import Profile


@dataclass
class Model:
    name: str
    width: float
    height: float
    verse: str | None
    profiles: list[Profile]
