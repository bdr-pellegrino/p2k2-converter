from pathlib import Path
from typing import Tuple, Dict
from ortools.linear_solver import pywraplp
from p2k2_converter.config import DEFAULT_CONFIG
import yaml
import logging

from p2k2_converter.p2k2 import BarBuilder, JobBuilder
from p2k2_converter.p2k2.classes import Job


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
    #   1. Each cut is used in exactly one bar
    #   2. The sum of the cuts used in each bar is less than or equal to the length of the bar
    for i in range(len(cuts)):
        solver.Add(sum(cuts_used[i, j, k] for j, (bar_length, num_bars) in enumerate(available_bars) for k in
                       range(num_bars)) == 1)

    for j, (bar_length, num_bars) in enumerate(available_bars):
        for k in range(num_bars):
            length = max(cuts[i].ol, cuts[i].il)
            solver.Add(sum(cuts_used[i, j, k] * length for i in range(len(cuts))) <= bar_length)

    # Objective: Maximize the utilization of bars
    total_utilization = 0

    for j, (bar_length, num_bars) in enumerate(available_bars):
        for k in range(num_bars):
            bar_utilization = sum(
                cuts_used[i, j, k] * max(cuts[i].ol, cuts[i].il) / bar_length for i in range(len(cuts))
            )
            total_utilization += bar_utilization

    solver.Maximize(total_utilization)
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


class Translator:

    def __init__(self, config_file: Path = DEFAULT_CONFIG):
        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def p2k2_translation(self, order, available_bars: Dict[str, Tuple[Tuple[int, int], ...]]) -> Job:
        logging.info(f"Translating order to P2K2 format")

        output_bars = []
        for model in order.models:
            translation = model.translate()

            for profile_name, bars in available_bars.items():
                cuts = translation[profile_name]
                allocations = optimize_cut_distribution(bars, cuts)

                profile = model.profiles[profile_name]
                for bar_length, cuts in allocations.items():
                    bar_builder = BarBuilder(brand=profile.brand, system=profile.system, profile_code=profile.code)
                    bar_builder.add_length(bar_length)
                    bar_builder.add_cuts(cuts)
                    output_bars.append(bar_builder.build())

        job_builder = JobBuilder()
        job_builder.add_bars(output_bars)
        return job_builder.build()



