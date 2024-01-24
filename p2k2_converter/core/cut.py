from dataclasses import dataclass


@dataclass
class Cut:
    length: int
    angleR: float | None
    angleL: float | None
