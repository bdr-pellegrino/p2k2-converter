import unittest
from p2k2_converter.pipeline.branch import Branch
from test.common import ArraySource, DummyDataExtractor, DummyDataMapper, DoubleMapper


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

    def test_execution_of_branch(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        with source.open() as opened_source:
            self.assertEqual(branch.execute(opened_source), 15)

    def test_cant_execute_branch_twice(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        with source.open() as opened_source:
            branch.execute(opened_source)
            with self.assertRaises(RuntimeError):
                branch.execute(opened_source)

    def test_ordered_execution_of_tests(self):
        branch = self.__branches["no_steps"]
        branch.add_step(DummyDataExtractor("data_extractor"))
        branch.add_step(DoubleMapper("double_mapper"))
        branch.add_step(DummyDataMapper("data_mapper"))
        source = ArraySource()
        with source.open() as opened_source:
            self.assertEqual(branch.execute(opened_source), 30)

        with self.assertRaises(TypeError):
            branch = self.__branches["with_steps"]
            branch.add_step(DoubleMapper("double_mapper"))
            with source.open() as opened_source:
                branch.execute(opened_source)

    def test_get_data_before_execution(self):
        branch = self.__branches["with_steps"]
        with self.assertRaises(RuntimeError):
            branch.get_result()

    def test_get_data_after_execution(self):
        branch = self.__branches["with_steps"]
        source = ArraySource()
        with source.open() as opened_source:
            branch.execute(opened_source)
            self.assertEqual(branch.get_result(), 15)

    def test_add_step_from_lambda(self):
        branch = Branch("lambda")
        branch.add_step(DummyDataExtractor("data_extractor"))
        branch.create_step_from_function("lambda_step", lambda s, d: [s, sum(d) * 2])
        source = ArraySource()
        with source.open() as opened_source:
            self.assertEqual(branch.execute(opened_source), 30)
