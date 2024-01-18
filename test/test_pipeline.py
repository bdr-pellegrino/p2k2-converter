import unittest
from .common import ArraySource, DummyDataExtractor, DoubleMapper, DummyDataMapper
from p2k2_converter.pipeline import Pipeline
from p2k2_converter.pipeline.branch import Branch


class PipelineTest(unittest.TestCase):

    def setUp(self):
        self.__components = {
            "source": ArraySource(),
            "branches": {
                "sum": Branch(
                    "Sum",
                    steps=[
                        DummyDataExtractor("Array data extractor"),
                        DummyDataMapper("Sum mapper"),
                    ]
                ),
                "double": Branch(
                    "Double Values",
                    steps=[
                        DummyDataExtractor("Array data extractor"),
                        DoubleMapper("Double values mapper"),
                    ]
                ),
            }
        }

    def test_add_branch(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = self.__components["branches"]["sum"]
        try:
            pipeline.add_branch(branch)
        except Exception:
            self.fail("add_branch() raised an Exception unexpectedly!")

    def test_add_branch_with_same_name(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = self.__components["branches"]["sum"]
        with self.assertRaises(ValueError):
            pipeline.add_branch(branch)
            pipeline.add_branch(branch)

    def test_add_branch_with_force(self):
        pipeline = Pipeline(source=ArraySource(), branches=[])
        branch = self.__components["branches"]["double"]
        try:
            pipeline.add_branch(branch)
            pipeline.add_branch(branch, force=True)
        except ValueError:
            self.fail("add_branch() raised ValueError unexpectedly!")

    def test_execute(self):
        pipeline = Pipeline(
            source=ArraySource(),
            branches=[
                self.__components["branches"]["sum"],
                self.__components["branches"]["double"],
            ]
        )

        try:
            pipeline.execute()
        except Exception:
            self.fail("execute() raised an Exception unexpectedly!")

    def test_cant_execute_twice(self):
        pipeline = Pipeline(
            source=ArraySource(),
            branches=[
                self.__components["branches"]["sum"],
                self.__components["branches"]["double"],
            ]
        )

        with self.assertRaises(RuntimeError):
            pipeline.execute()
            pipeline.execute()

    def test_get_with_invalid_name(self):
        pipeline = Pipeline(
            source=ArraySource(),
            branches=[
                self.__components["branches"]["sum"],
                self.__components["branches"]["double"],
            ]
        )

        with self.assertRaises(ValueError):
            pipeline.execute()
            pipeline.get("Invalid name")

    def test_get(self):
        pipeline = Pipeline(
            source=ArraySource(),
            branches=[
                self.__components["branches"]["sum"],
                self.__components["branches"]["double"],
            ]
        )

        try:
            pipeline.execute()
            pipeline.get("Sum")
            pipeline.get("Double Values")
        except ValueError | RuntimeError:
            self.fail("get() raised an Exception unexpectedly!")

