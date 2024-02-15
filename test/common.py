from contextlib import contextmanager
from p2k2_converter.pipeline.source import BaseSource
from p2k2_converter.pipeline.step import BaseStep
from p2k2_converter.core.classes import Buyer, Order, Profile, Bar, Cut, Model


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


def define_order(number_of_models: int, number_of_profiles: int, number_of_bars: int, number_of_cuts: int):
    buyer = Buyer(
        full_name="John Doe",
        email="jdoe@someemail.it",
        phone="051 123456",
        cell_phone="333 123456",
        address="Via Roma 1",
        city="Bologna"
    )

    models = []
    for i in range(number_of_models):
        model = Model(name=f"Model_{i}", width=1000, height=1000)

        profiles = dict()
        for l in range(number_of_profiles):
            profile = Profile(brand="Brand", system="System", code=f"PELLEGRINO_PROF_{l}")

            for j in range(number_of_bars):
                bar = Bar(serial_code=f"BAR_{j}", length=6000)

                for k in range(number_of_cuts):
                    cut = Cut(length=1000, angleL=90, angleR=90)
                    bar.cuts.append(cut)

                profile.bars.append(bar)

            profiles[f"PELLEGRINO_PROF_{l}"] = profile

        model.profiles = profiles
        models.append(model)

    return Order(buyer=buyer, models=models)
