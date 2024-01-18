from p2k2_converter.pipeline.branch import Branch
from p2k2_converter.pipeline.source import BaseSource


class Pipeline:
    def __init__(self, source: BaseSource, branches: list[Branch]):
        self.__source = source

        self.__branches = {}
        for branch in branches:
            self.__branches[branch.get_name()] = branch

    def execute(self):
        with self.__source.open() as resource:
            for branch in self.__branches.values():
                branch.execute(resource)
