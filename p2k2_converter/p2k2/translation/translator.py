from pathlib import Path
from typing import Tuple
from p2k2_converter.config import DEFAULT_CONFIG
import yaml
import logging
from ortools.linear_solver import pywraplp


def optimize_cut_distribution(available_bars, cuts,
                              solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('SCIP')):
    """
    Optimize the distribution of cuts in the available bars.

    Args:
        available_bars: A tuple of tuples, where each of thesr contains the
                        length of the rod and the number of bars to use
        cuts: A list of the cuts to be distributed
        solver: The solver to use for the optimization problem

    Returns:
        A dictionary of the cuts used in each rod
    """
    cuts_used = {}
    for i in range(len(cuts)):
        for j in range(len(available_bars)):
            cuts_used[i, j] = solver.BoolVar('Cut_%i_in_Rod_%i' % (i, j))

    # Constraints:
    #   1. Each cut is used in exactly one rod
    #   2. The sum of the cuts used in each rod is less than or equal to the length of the rod
    for i in range(len(cuts)):
        solver.Add(sum(cuts_used[i, j] for j, _ in enumerate(available_bars)) == 1)

    for j, rod_info in enumerate(available_bars):
        rod_length, num_bars = rod_info
        solver.Add(sum(cuts_used[i, j] * cuts[i] for i, _ in enumerate(cuts)) <= rod_length * num_bars)

    # Objective: Maximize the utilization of rods
    total_utilization = sum(sum(cuts_used[i, j] * cuts[i] / rod_length for i, _ in enumerate(cuts))
                            for j, (rod_length, _) in enumerate(available_bars))
    solver.Maximize(total_utilization)
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        remaining_lengths = []
        for j, (rod_length, _) in enumerate(available_bars):
            total_cut_length = sum(cuts_used[i, j].solution_value() * cuts[i] for i, _ in enumerate(cuts))
            remaining_length = rod_length - total_cut_length
            if remaining_length > 0:
                remaining_lengths.append((j, remaining_length))
        return cuts_used, tuple(remaining_lengths)
    else:
        raise Exception("Can't find a distribution for the cuts.")

    pass


class Translator:

    def __init__(self, config_file: Path = DEFAULT_CONFIG):
        with open(config_file, "r") as file:
            self.__config_file = yaml.safe_load(file)

    def p2k2_translation(self, order, available_bars: Tuple[Tuple[int, int], ...]):
        logging.info(f"Translating order to P2K2 format")

        cut_list = []
        for model in order.models:
            cut_list += [cut for cut_list in model.translate().values() for cut in cut_list]

        cut_lengths = [max(cut.il, cut.ol) for cut in cut_list]

        print(optimize_cut_distribution(available_bars, cut_lengths))
