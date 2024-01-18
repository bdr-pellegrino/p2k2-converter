import unittest
from .common import ArraySource, DummyDataExtractor, DoubleMapper, DummyDataMapper
from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch


class PipelineTest(unittest.TestCase):
    def test_add_branch(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = Branch(
            "Double Values",
            steps=[
                DummyDataExtractor("Array data extractor"),
                DoubleMapper("Double values mapper"),
            ]
        )

        try:
            pipeline.add_branch(branch)
        except ValueError:
            self.fail("add_branch() raised ValueError unexpectedly!")

    def test_add_branch_with_same_name(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = Branch(
            "Double Values",
            steps=[
                DummyDataExtractor("Array data extractor"),
                DoubleMapper("Double values mapper"),
            ]
        )

        with self.assertRaises(ValueError):
            pipeline.add_branch(branch)
            pipeline.add_branch(branch)

    def test_add_branch_with_force(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = Branch(
            "Double Values",
            steps=[
                DummyDataExtractor("Array data extractor"),
                DoubleMapper("Double values mapper"),
            ]
        )

        try:
            pipeline.add_branch(branch)
            pipeline.add_branch(branch, force=True)
        except ValueError:
            self.fail("add_branch() raised ValueError unexpectedly!")


