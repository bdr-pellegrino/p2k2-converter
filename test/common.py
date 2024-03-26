from contextlib import contextmanager
from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import BaseStep
from p2k2_converter.p2k2.classes import Cut as P2K2Cut
from p2k2_converter.core.classes import Buyer, Order, Profile, Cut, Model


class ArraySource(BaseSource):
    @contextmanager
    def open(self):
        yield [1, 2, 3, 4, 5]


class DummyDataExtractor(BaseStep):
    def execute(self, source, data):
        return [source, source]


class DummyDataMapper(BaseStep):
    def execute(self, source, data):
        return [source, sum(data)]


class DoubleMapper(BaseStep):
    def execute(self, source, data):
        doubled_data = [x * 2 for x in data]
        return [source, doubled_data]


def __define_translation_from_order(model):
    def translation():
        cuts = {}
        for profile in model.profiles.values():
            for cut in profile.cuts:
                if profile.code not in cuts:
                    cuts[profile.code] = []

                cuts[profile.code].append(P2K2Cut(
                    il=cut.length,
                    ol=cut.length,
                    angl=cut.angleL,
                    angr=cut.angleR
                ))

        return cuts

    return translation


def define_order(config):

    if "buyer" not in config:
        raise ValueError("Buyer information is missing from the configuration")

    buyer = Buyer(
        full_name=config["buyer"]["full_name"],
        address=config["buyer"]["address"],
        email=config["buyer"]["email"],
        phone=config["buyer"]["phone"],
        cell_phone=config["buyer"]["cell_phone"],
        city=config["buyer"]["city"],
    )

    if "models" not in config:
        raise ValueError("Models information is missing from the configuration")

    models = []
    for i, model_data in enumerate(config["models"]):

        name = model_data["name"] if "name" in model_data else f"Model_{i}"
        model = Model(name=name, width=model_data["width"], height=model_data["height"])

        if "profiles" not in model_data:
            raise ValueError(f"Profiles information is missing from the configuration for model {name}")

        profiles = {}
        for profile_data in model_data["profiles"]:
            if "cuts" not in profile_data:
                raise ValueError(f"Cuts information is missing from the configuration for profile {profile_data['name']}")

            profile = Profile(
                system=profile_data["system"],
                code=profile_data["code"],
                length=profile_data["length"]
            )

            for cut in profile_data["cuts"]:
                cut = Cut(
                    length=cut["length"],
                    angleL=cut["angle_left"],
                    angleR=cut["angle_right"],
                    height=cut["height"]
                )
                profile.cuts.append(cut)

            profiles[profile.code] = profile

        model.profiles = profiles
        model.set_translation_strategy(__define_translation_from_order(model))
        models.append(model)

    return config["bars"], Order(buyer=buyer, models=models)
