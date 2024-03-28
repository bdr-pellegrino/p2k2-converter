from typing import List, Dict
from p2k2_converter.p2k2.classes import Machining as P2k2Machining
from p2k2_converter.core.classes import Model, Machining
from p2k2_converter.p2k2 import CutBuilder
from p2k2_converter.core.utils.sentence import Sentence


def __machining_application_index(dim: int, machinings: List[Machining], offset: int) -> Dict[int, List[Machining]]:
    """
    Calculate how to distribute the profile machinings to the cuts.

    Args:
        dim: The dimension (width or height) of the cut.
        machinings: List of machinings to apply.
        offset: The offset.

    Returns:
        A dictionary where the index refers to the cut index, and the value is a list of machinings
        to apply to the specific cut.
    """
    base = 0
    top = dim
    cut_index = 0

    output = {}
    for machining in sorted(machinings, key=lambda mach: mach.offset):
        while not (base <= machining.offset <= top):
            base = top
            top += dim
            cut_index += 1

        output.setdefault(cut_index, []).append(P2k2Machining(machining.code, offset))

    return output


def configure_cuts_for_profile(builders: List[CutBuilder], machinings: List[Machining], dim: int, offset: int,
                               refinement: int = 0) -> List[CutBuilder]:
    """
    Configure the cuts to add in the profile.

    Args:
        builders: The list of cut builders used to create the cuts
        machinings: The list of machinings to be distributed
        dim: Working dimension
        offset: Offset of the machining
        refinement: The left trim of the bar.

    Returns:
        A list of configured P2k2 cuts
    """
    cut_list = []
    machining_distribution = __machining_application_index(dim, machinings, offset)

    for idx, cut in enumerate(builders):
        if idx in machining_distribution:
            for machining in machining_distribution[idx]:
                cut.add_machining_item(machining)

        if idx == len(builders) - 1 and refinement != 0:
            cut.add_left_trim_cut_length(refinement)

        cut_list.append(cut)

    return cut_list


def profile_name(model: Model, profile_code: str) -> str:
    """
    Create a string containing the profile name

    Args:
        model: Model of the profile
        profile_code: The profile code

    Returns:

    """
    return f"{model.name}_{profile_code}"


__all__ = ["Sentence", "profile_name", "configure_cuts_for_profile"]
