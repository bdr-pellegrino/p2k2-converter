import unittest
import yaml

from p2k2_converter.core.workflow import Moderna
from p2k2_converter.pipeline.source import XlsmSource
from p2k2_converter.config import DEFAULT_CONFIG
from test.data.moderna import WORKSHEET, IN_STOCK_FLAG_WORKSHEET


class TestModernaWorkflow(unittest.TestCase):

    def setUp(self):
        self.__test_files = {
            "product_worksheet": WORKSHEET,
            "in_stock_worksheet": IN_STOCK_FLAG_WORKSHEET,
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
                "r_angle": 0,
                "machinings": {
                    "FORO DOGA": [(0, 0, 0, 0), (0, 3)],
                }
            },

            "CERNIERA TUBOLARE": {
                "cuts_quantity": 1,
                "cuts_length": 813,
                "l_angle": 90,
                "r_angle": 90,
                "machinings": {
                    "MACHINING CERNIERA TUBOLARE": [tuple([0]), tuple([0])],
                }
            },

            "CERNIERA APERTA": {
                "cuts_quantity": 1,
                "cuts_length": 812.5,
                "l_angle": 0,
                "r_angle": 0,
                "machinings": {
                    "MACHINING CERNIERA APERTA": [tuple([0]), tuple([0])],
                }
            },

            "PROFILO GANCIO-UNCINO": {
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
                "machinings": {
                    "MACHINING H": [tuple([0]), tuple([0])],
                }
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

    def test_ignore_in_stock_profiles(self):
        source = XlsmSource(self.__test_files["in_stock_worksheet"])
        with source.open() as src:
            _, model = self.__moderna_workflow.profiles_definition(
                *self.__moderna_workflow.model_definition(src, None)
            )

            self.assertIn("PROFILO DOGA", model.profiles)
            self.assertIn("PROFILO GANCIO-UNCINO", model.profiles)
            self.assertNotIn("CERNIERA TUBOLARE", model.profiles)
            self.assertNotIn("CERNIERA APERTA", model.profiles)
            self.assertNotIn("H", model.profiles)


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

    def test_machining_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__moderna_workflow.machining_definition(
                *self.__moderna_workflow.cuts_definition(
                    *self.__moderna_workflow.profiles_definition(
                        *self.__moderna_workflow.model_definition(src, None)
                    )
                )
            )

        for profile_name in self.__expected_configuration:
            profile_configuration = self.__expected_configuration[profile_name]
            profile = model.profiles[profile_name]
            machinings = profile.machinings
            if "machinings" in profile_configuration:
                codes = list(profile_configuration["machinings"].keys())
                current_codes = sorted(set(machining.code for machining in machinings))

                self.assertEqual(current_codes, codes)

                for code, machining_configuration in profile_configuration["machinings"].items():
                    if len(machining_configuration) > 0:
                        offsets = list(machining_configuration[0])
                        current_offsets = [machining.offset for machining in machinings if machining.code == code]
                        self.assertEqual(current_offsets, offsets)

    def test_translation_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__moderna_workflow.translation_definition(
                *self.__moderna_workflow.machining_definition(
                    *self.__moderna_workflow.cuts_definition(
                        *self.__moderna_workflow.profiles_definition(
                            *self.__moderna_workflow.model_definition(src, None)
                        )
                    )
                )
            )

            for name, cuts in model.translate().items():
                self.assertEqual(len(cuts), self.__expected_configuration[name]["cuts_quantity"])
                for i, cut in enumerate(cuts):
                    if cut.machinings:
                        for machining in cut.machinings.machining:
                            self.assertIn(i, self.__expected_configuration[name]["machinings"][machining.wcode][1])

