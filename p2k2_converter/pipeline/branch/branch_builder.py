from p2k2_converter.pipeline.branch import Branch
from p2k2_converter.pipeline.step import BaseStep


class BranchBuilder:
    def __init__(self, branch_name: str):
        self.branch = Branch(branch_name)

    def add_step(self, step: BaseStep):
        self.branch.add_step(step)
        return self

    def add_from_lambda(self, name: str, step):
        self.branch.create_step_from_lambda(name, step)
        return self

    def build(self):
        return self.branch
