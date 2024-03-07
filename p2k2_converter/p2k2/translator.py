import logging
from typing import List
from p2k2_converter.core.classes import Order, Profile
from p2k2_converter.p2k2 import BarBuilder, CutBuilder, JobBuilder
from p2k2_converter.p2k2.classes import Bar, Job
import yaml

class Translator:

    def __init__(self, config_file: str):
        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def p2k2_translation(self, order: Order):
        logging.info("Translating order to P2K2 format")

        job_builder = JobBuilder()

        for model in order.models:
            model_configuration = self.__config_file[model.name]
            for profile_name, profile in model.profiles.items():
                profile_configurations = model_configuration["profiles"]
                default_bar_length = next(
                    (p["bar-length"] for p in profile_configurations if p["code"] == profile_name), None
                )

                bars = self.__define_bars(profile_name, profile, default_bar_length)
                job_builder.add_bars(bars)
            return job_builder.build()

    def __define_bars(self, profile_name: str, profile: Profile, default_bar_length: int) -> List[Bar]:
        cuts = profile.cuts

        bars = []
        bar_length = default_bar_length
        bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
        bar_builder.add_length(bar_length)

        for cut in cuts:
            cut_builder = CutBuilder()
            if cut.length > bar_length:
                bars.append(bar_builder.build())
                bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
                bar_builder.add_length(bar_length)

            cut_builder.add_cut_length(cut.length)
            cut_builder.add_left_cutting_angle(cut.angleL)
            cut_builder.add_right_cutting_angle(cut.angleR)

            bar_builder.add_cut(cut_builder.build())

        bars.append(bar_builder.build())

        return bars

