import logging
from typing import Dict, Tuple
from ortools.linear_solver import pywraplp
from .. import BarBuilder, JobBuilder
from ..classes import Job


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
            for k in range(num_bars):
                cuts_used[i, j, k] = solver.BoolVar('Cut_%i_in_Bar_%i_%i' % (i, j, k))

    # Constraints:
    #   1. Each cut is used in at most one bar
    #   2. The sum of the cuts used in each bar is less than or equal to the length of the bar
    for i in range(len(cuts)):
        solver.Add(sum(cuts_used[i, j, k] for j, (bar_length, num_bars) in enumerate(available_bars) for k in
                       range(num_bars)) <= 1)

    for j, (bar_length, num_bars) in enumerate(available_bars):
        for k in range(num_bars):
            bar_cuts_length = [max(cuts[i].ol, cuts[i].il) for i in range(len(cuts))]
            total_length = sum(bar_cuts_length)
            solver.Add(sum(cuts_used[i, j, k] * bar_cuts_length[i] for i in range(len(cuts))) <= bar_length)

    # Objective: Maximize the number of cuts used
    total_cuts_used = sum(cuts_used[i, j, k] for i in range(len(cuts))
                          for j, (bar_length, num_bars) in enumerate(available_bars)
                          for k in range(num_bars))

    solver.Maximize(total_cuts_used)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        bar_cuts_map = {}
        for i in range(len(cuts)):
            for j, (bar_length, num_bars) in enumerate(available_bars):
                for k in range(num_bars):
                    if cuts_used[i, j, k].solution_value() > 0:
                        if bar_length not in bar_cuts_map:
                            bar_cuts_map[bar_length] = []
                        bar_cuts_map[bar_length].append(cuts[i])

        return bar_cuts_map
    else:
        raise Exception("Can't find a distribution for the cuts.")


def p2k2_translation(available_bars: Dict[str, Tuple[Tuple[int, int], ...]], order) -> Job:
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

        for profile_name, cuts in translation.items():
            if profile_name not in cuts_for_profile:
                cuts_for_profile[profile_name] = cuts
            else:
                cuts_for_profile[profile_name] += cuts

    for profile_name, bars in available_bars.items():
        profile = next((model.profiles[profile_name] for model in order.models if profile_name in model.profiles), None)
        if profile is None:
            raise Exception(f"Profile {profile_name} not found in the order.")

        allocations = optimize_cut_distribution(bars, cuts_for_profile[profile_name])
        for bar_length, cuts in allocations.items():
            bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
            bar_builder.add_length(bar_length)
            bar_builder.add_cuts(cuts)
            output_bars.append(bar_builder.build())

    job_builder = JobBuilder()
    job_builder.add_bars(output_bars)
    return job_builder.build()


__all__ = ["optimize_cut_distribution", "p2k2_translation"]
