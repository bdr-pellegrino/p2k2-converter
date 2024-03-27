import unittest
import yaml

from p2k2_converter.core.workflow import Moderna
from p2k2_converter.pipeline.source import XlsmSource
from p2k2_converter.config import DEFAULT_CONFIG
from test.data.moderna import WORKSHEET


class TestModernaWorkflow(unittest.TestCase):

    def setUp(self):
        self.__test_files = {
            "product_worksheet": WORKSHEET,
            "config_file": DEFAULT_CONFIG
        }

        with open(self.__test_files["config_file"], "r") as file:
            self.__profile_config = yaml.safe_load(file)

        self.__moderna_workflow = Moderna(row=8, config_file=self.__profile_config)

    def test_model_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            workbook, model = self.__moderna_workflow.model_definition(src, None)

            self.assertEqual(model.name, "MODERNA")
            self.assertEqual(model.width, 100)
            self.assertEqual(model.height, 80)


