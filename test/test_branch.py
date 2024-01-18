import unittest
from p2k2_converter.pipeline.branch import Branch
from .common import ArraySource, DummyDataExtractor, DummyDataMapper, DoubleMapper


class BranchTest(unittest.TestCase):

    def setUp(self):
        self.__branches = {
            "no_steps": Branch("no_steps"),
            "with_steps": Branch("with_steps", steps=[
                DummyDataExtractor("data_extractor"),
                DummyDataMapper("data_mapper")
            ])
        }

    def test_get_branch_name(self):
        self.assertEqual(self.__branches["no_steps"].get_name(), "no_steps")

    def test_add_data_extractor(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataExtractor("data_extractor"))
        self.assertEqual(branch.get_steps()["extractor"].get_name(), "data_extractor")

    def test_cant_add_two_data_extractor_without_force(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataExtractor("data_extractor"))
        with self.assertRaises(ValueError):
            branch.add_step(DummyDataExtractor("data_extractor"))

    def test_can_add_two_data_extractor_with_force(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataExtractor("data_extractor"))
        branch.add_step(DummyDataExtractor("data_extractor_2"), force=True)
        self.assertEqual(branch.get_steps()["extractor"].get_name(), "data_extractor_2")

    def test_add_data_mapper(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataMapper("data_mapper"))
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")

    def test_cant_add_two_data_mapper_with_same_name_without_force(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataMapper("data_mapper"))
        with self.assertRaises(ValueError):
            branch.add_step(DummyDataMapper("data_mapper"))

    def test_can_add_two_data_mapper_with_same_name_with_force(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataMapper("data_mapper"))
        branch.add_step(DummyDataMapper("data_mapper"), force=True)
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")

    def test_defensive_copy_of_steps(self):
        branch = self.__branches["with_steps"]
        steps = branch.get_steps()
        steps["mappers"]["data_mapper"] = None
        self.assertEqual(branch.get_steps()["mappers"]["data_mapper"].get_name(), "data_mapper")

    def test_execution_of_branch(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        self.assertEqual(branch.execute(source), 15)

    def test_cant_execute_branch_twice(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        branch.execute(source)
        with self.assertRaises(RuntimeError):
            branch.execute(source)

    def test_ordered_execution_of_tests(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataExtractor("data_extractor"))
        branch.add_step(DoubleMapper("double_mapper"))
        branch.add_step(DummyDataMapper("data_mapper"))
        source = ArraySource()
        self.assertEqual(branch.execute(source), 30)

        with self.assertRaises(TypeError):
            branch = self.__branches["with_steps"]
            branch.add_step(DoubleMapper("double_mapper"))
            branch.execute(source)

    def test_get_data_before_execution(self):
        branch = self.__branches["with_steps"]
        with self.assertRaises(RuntimeError):
            branch.get_data()

    def test_get_data_after_execution(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        branch.execute(source)
        self.assertEqual(branch.get_data(), 15)
    