from dataclasses import dataclass
from p2k2_converter.core import Model


@dataclass
class Order:
    name: str
    models: list[Model]
