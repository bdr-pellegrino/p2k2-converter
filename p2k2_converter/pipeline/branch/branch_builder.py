from typing import Callable, TypeVar
from p2k2_converter.pipeline.branch import Branch
from p2k2_converter.pipeline.step import BaseStep
from p2k2_converter.core.utils import Sentence

T = TypeVar("T")
Q = TypeVar("Q")


class BranchBuilder:
    def __init__(self, branch_name: str):
        self.branch = Branch(branch_name)

    def add_step(self, step: BaseStep):
        self.branch.add_step(step)
        return self

    def add_from_function(self, step: Callable[[T, any], Q]):
        self.branch.create_step_from_function(Sentence(step.__name__).pascal_case(), step)
        return self

    def build(self):
        return self.branch
