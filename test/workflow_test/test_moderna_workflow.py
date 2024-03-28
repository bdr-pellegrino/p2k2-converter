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
        self.__expected_configuration = {
            "PROFILO DOGA": {
                "cuts_quantity": 4,
                "cuts_length": 806,
                "l_angle": 0,
                "r_angle": 0
            },

            "CERNIERA TUBOLARE": {
                "cuts_quantity": 1,
                "cuts_length": 813,
                "l_angle": 90,
                "r_angle": 90,
            },

            "CERNIERA APERTA": {
                "cuts_quantity": 1,
                "cuts_length": 812.5,
                "l_angle": 0,
                "r_angle": 0,
            },

            "PROFILO GANCIO\\UNCINO": {
                "cuts_quantity": 1,
                "cuts_length": 812.5,
                "l_angle": 0,
                "r_angle": 0
            },

            "H": {
                "cuts_quantity": 1,
                "cuts_length": 813,
                "l_angle": 0,
                "r_angle": 0,
            },

            "TENUTA LATERALE": {
                "cuts_quantity": 0,
                "cuts_length": 823,
                "l_angle": 0,
                "r_angle": 0,
            }
        }

    def test_model_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            workbook, model = self.__moderna_workflow.model_definition(src, None)

            self.assertEqual(model.name, "MODERNA")
            self.assertEqual(model.width, 100)
            self.assertEqual(model.height, 80)

    def test_check_profiles(self):
        source = XlsmSource(self.__test_files["product_worksheet"])
        checked_profiles = []

        with source.open() as src:
            _, model = self.__moderna_workflow.profiles_definition(
                *self.__moderna_workflow.model_definition(src, None)
            )

            profiles = list(self.__expected_configuration.keys())
            for code in model.profiles:
                self.assertIn(code, profiles)
                del self.__expected_configuration[code]
                checked_profiles.append(code)

            self.assertEqual(checked_profiles, profiles)

    def test_cuts_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__moderna_workflow.cuts_definition(
                *self.__moderna_workflow.profiles_definition(
                    *self.__moderna_workflow.model_definition(src, None)
                )
            )

            for profile_name in self.__expected_configuration:
                profile_configuration = self.__expected_configuration[profile_name]
                cuts = model.profiles[profile_name].cuts

                self.assertEqual(len(cuts), profile_configuration["cuts_quantity"])

                cut_length = profile_configuration["cuts_length"]
                angle_left = profile_configuration["l_angle"]
                angle_right = profile_configuration["r_angle"]
                for cut in cuts:
                    self.assertEqual(cut.length, cut_length)
                    self.assertEqual(cut.angleL, angle_left)
                    self.assertEqual(cut.angleR, angle_right)



