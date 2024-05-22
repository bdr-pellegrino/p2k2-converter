import logging
from typing import Dict, Tuple
from ortools.linear_solver import pywraplp
from p2k2_converter.p2k2 import BarBuilder, JobBuilder, CutBuilder
from p2k2_converter.p2k2.classes import Job


class Translation:
    def __init__(self, model, order_id, client_id, cell_row):
        self.__translation_map = {}
        self.__model = model
        self.__order_id = order_id
        self.__client_id = client_id
        self._cell_row = cell_row

    def get_translation_map(self):
        """
        Get the translation map of the model.

        Returns:
            The translation map of the model
        """
        return self.__translation_map

    def add_profile_translation(self, profile_code, translation):
        """
        Add a translation function for a profile of the model.

        Args:
            profile_code: The code of the profile to translate
            translation: The translation function to use for the profile
        """
        self.__translation_map[profile_code] = translation

    def translate_profile(self, profile_code):
        """
        Translate a profile of the model in the P2K2 format.

        Args:
            profile_code: The code of the profile to translate

        Returns:
            A tuple of P2k2Cut instances representing the profile in the P2K2 format
        """
        profile = self.__model.profiles[profile_code]
        cuts, machining = profile.cuts, profile.machinings
        builders = [
            CutBuilder().add_cut_length(cut.length)
            .add_left_cutting_angle(cut.angleL)
            .add_right_cutting_angle(cut.angleR)
            for cut in cuts
        ]

        translation_function = self.__translation_map.get(profile_code)

        return translation_function(profile, self.__apply_labels(builders), cuts, machining)

    def translate(self):
        """
        Translate all profiles of the model in the P2K2 format.
        """
        translation = {}
        for profile_code in self.__translation_map.keys():
            translation[profile_code] = self.translate_profile(profile_code)
        return translation

    def __apply_labels(self, builders):
        """
        Apply the labels to the cuts.

        Args:
            builders: The list of cut builders
            workbook: The workbook instance

        Returns:
            The list of cut builders with the labels applied
        """
        cut_list = []
        for builder in builders:
            builder.add_label(
                f"{self.__model.name} ORDER ID {self.__order_id}")
            builder.add_label(
                f"{self.__model.name} CLIENT ID {self.__client_id}")
            builder.add_label(f"ROW {self._cell_row}")
            cut_list.append(builder)

        return tuple(cut_list)


def optimize_cut_distribution(available_bars, cuts,
                              solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')):
    """
    Optimize the distribution of cuts in the available bars.

    Args:
        available_bars: A tuple of tuples, where each of these contains the
                        length of a bar and the quantity of that bar.
        cuts: A list of the cuts to be distributed
        solver: The solver to use for the optimization problem

    Returns:
        A dictionary of the cuts used in each Bar
    """
    cuts_used = {}
    for i in range(len(cuts)):
        for j, (bar_length, num_bars) in enumerate(available_bars):
            for k in range(int(num_bars)):
                cuts_used[i, j, k] = solver.BoolVar('Cut_%i_in_Bar_%i_%i' % (i, j, k))

    for i in range(len(cuts)):
        solver.Add(sum(cuts_used[i, j, k] for j, (bar_length, num_bars) in enumerate(available_bars) for k in
                       range(int(num_bars))) <= 1)

    for j, (bar_length, num_bars) in enumerate(available_bars):
        for k in range(int(num_bars)):
            bar_cuts_length = [max(cuts[i].ol, cuts[i].il) for i in range(len(cuts))]
            solver.Add(sum(cuts_used[i, j, k] * bar_cuts_length[i] for i in range(len(cuts))) <= bar_length)

    total_cuts_used = sum(cuts_used[i, j, k] for i in range(len(cuts))
                          for j, (bar_length, num_bars) in enumerate(available_bars)
                          for k in range(int(num_bars)))

    solver.Maximize(total_cuts_used)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        bar_cuts_map = {}
        for i in range(len(cuts)):
            for j, (bar_length, num_bars) in enumerate(available_bars):
                if bar_length not in bar_cuts_map:
                    bar_cuts_map[bar_length] = []
                    for k in range(int(num_bars)):
                        bar_cuts_map[bar_length].append([])
                for k in range(int(num_bars)):
                    if cuts_used[i, j, k].solution_value() > 0:
                        bar_cuts_map[bar_length][k].append(cuts[i])
        return bar_cuts_map
    else:
        raise Exception("Can't find a distribution for the cuts.")


def p2k2_translation(available_bars: Dict[str, Dict[str, Tuple[Tuple[int, int], ...]]], order) -> Job:
    """
    Translate the order to the P2K2 format.
    Args:
        order: The order to be translated
        available_bars: The available bars to be used in the translation

    Returns:

    """
    logging.info(f"Translating order to P2K2 format")

    output_bars = []
    cuts_for_profile = {}

    for model in order.models:
        translation = model.translate()

        profiles = cuts_for_profile.get(model.name, {})
        for profile_code, cuts in translation.items():
            if profile_code not in profiles:
                profiles[profile_code] = cuts
            else:
                profiles[profile_code] += cuts

        cuts_for_profile[model.name] = profiles

    for model_name, translation in cuts_for_profile.items():
        for profile_code, cuts in translation.items():
            bars = available_bars[model_name][profile_code]
            allocations = optimize_cut_distribution(bars, cuts)
            model = next(
                (model for model in order.models if model.name == model_name),
                None
            )
            if model is None:
                raise Exception(f"Model {model_name} not found in the order.")
            profile = next(
                (profile_info for code, profile_info in model.profiles.items() if code == profile_code),
                None
            )
            if profile is None:
                raise Exception(f"Profile {profile_code} not found in the order.")

            for bar_length, output_cuts in allocations.items():
                for bar_cuts in output_cuts:
                    bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
                    bar_builder.add_length(bar_length)
                    bar_builder.add_cuts(bar_cuts)
                    output_bars.append(bar_builder.build())

    job_builder = JobBuilder()
    job_builder.add_bars(output_bars)
    return job_builder.build()


__all__ = ["optimize_cut_distribution", "p2k2_translation", "Translation"]
