from typing import List

from p2k2_converter.core.classes import Order, Profile
from p2k2_converter.p2k2 import BarBuilder, CutBuilder, JobBuilder
from p2k2_converter.p2k2.classes import Bar, Job


class Translator:

    def p2k2_translation(self, order: Order) -> Job:
        job_builder = JobBuilder()

        for model in order.models:

            for profile_name, profile in model.profiles.items():
                bars = self.__define_bars(profile)
                for bar in bars:
                    job_builder.add_bar(bar)

        return job_builder.build()

    def __define_bars(self, profile: Profile) -> List[Bar]:
        machinings = profile.machinings
        profile_bars = profile.bars

        base = 0
        bars = []
        for bar in profile_bars:
            bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
            bar_builder.add_length(bar.length)
            profile_cuts = bar.cuts

            for cut in profile_cuts:
                cut_builder = CutBuilder()

                cut_builder.add_cut_length(cut.length) \
                    .add_left_cutting_angle(cut.angleL) \
                    .add_right_cutting_angle(cut.angleR)

                top = base + cut.length

                while machinings and base <= machinings[0].offset <= top:
                    current_machining = machinings.pop(0)
                    offset = current_machining.offset - base
                    cut_builder.add_machining(current_machining.code, offset)

                bar_builder.add_cut(cut_builder.build())
                base = top

            bars.append(bar_builder.build())

        return bars

