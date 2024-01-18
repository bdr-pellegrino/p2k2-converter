import unittest
from p2k2_converter.pipeline.branch import Branch
from .common import ArraySource, DummyDataExtractor, DummyDataMapper


class BranchTest(unittest.TestCase):

    def test_get_branch_name(self):
        branch = Branch("test_branch")
        self.assertEqual(branch.get_name(), "test_branch")

    def test_add_data_extractor(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataExtractor("data_extractor"))
        self.assertEqual(branch.get_steps()["extractor"].get_name(), "data_extractor")

    def test_cant_add_two_data_extractor_without_force(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataExtractor("data_extractor"))
        with self.assertRaises(ValueError):
            branch.add_step(DummyDataExtractor("data_extractor"))

    def test_can_add_two_data_extractor_with_force(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataExtractor("data_extractor"))
        branch.add_step(DummyDataExtractor("data_extractor_2"), force=True)
        self.assertEqual(branch.get_steps()["extractor"].get_name(), "data_extractor_2")

    def test_add_data_mapper(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataMapper("data_mapper"))
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")

    def test_cant_add_two_data_mapper_with_same_name_without_force(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataMapper("data_mapper"))
        with self.assertRaises(ValueError):
            branch.add_step(DummyDataMapper("data_mapper"))

    def test_can_add_two_data_mapper_with_same_name_with_force(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataMapper("data_mapper"))
        branch.add_step(DummyDataMapper("data_mapper"), force=True)
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")

    def test_defensive_copy_of_steps(self):
        branch = Branch("test_branch")
        branch.add_step(DummyDataMapper("data_mapper"))
        steps = branch.get_steps()
        steps["mappers"]["data_mapper"] = None
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")


