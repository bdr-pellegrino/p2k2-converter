from dataclasses import dataclass
from p2k2_converter.core import Model
from copy import deepcopy as copy


@dataclass
class Order:
    name: str
    models: list[Model]

    def add_model(self, model: Model) -> None:
        self.models.append(model)

    def remove_model(self, model: Model) -> None:
        self.models.remove(model)

    def get_models(self) -> list[Model]:
        return copy(self.models)
