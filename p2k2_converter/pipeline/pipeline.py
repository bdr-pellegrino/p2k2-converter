from p2k2_converter.pipeline.branch import Branch
from p2k2_converter.pipeline.source import BaseSource
from typing import TypeVar

T = TypeVar("T")


class Pipeline:
    def __init__(self, branches: list[Branch] = None, source: BaseSource = None):
        self.__source = source
        self.__branches = {}
        for branch in branches:
            self.__branches[branch.get_name()] = branch
        self.__executed = False

    def set_source(self, source: BaseSource) -> None:
        self.__source = source

    def add_branch(self, branch: Branch, force: bool = False) -> None:
        if branch.get_name() in self.__branches and not force:
            raise ValueError("Branch already set for this pipeline")
        self.__branches[branch.get_name()] = branch

    def execute(self) -> None:
        if self.__executed:
            raise RuntimeError("Pipeline already executed")
        try:
            for branch in self.__branches.values():
                branch.execute(self.__source)
            self.__executed = True
        except Exception as e:
            self.__executed = False

    def get(self, name: str) -> T:
        if name not in self.__branches.keys():
            raise ValueError("Branch not found")
        else:
            return self.__branches[name].get_result()
