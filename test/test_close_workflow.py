import unittest
from p2k2_converter.core.workflow.close import Close
from p2k2_converter.pipeline.source import XlsmSource
from p2k2_converter.config import DEFAULT_CONFIG
from test.data.close import WORKSHEET

import yaml


class TestCloseWorkflow(unittest.TestCase):

    def setUp(self):
        self.__test_files = {
            "product_worksheet": WORKSHEET,
            "config_file": DEFAULT_CONFIG
        }

        with open(self.__test_files["config_file"], "r") as file:
            self.__profile_config = yaml.safe_load(file)

        self.__close_workflow = Close(
            row=8,
            config_file=self.__profile_config
        )
        self.__profile_config = {
            "PROFILO DOGA": {
                "cuts_quantity": 10,
                "cuts_length": 741,
                "l_angle": 90,
                "r_angle": 90,
                "machinings": {
                    "CERNIERA FORO ANTA": [115, 138, 920, 943, 520, 543],
                    "FORO SCASSI TELAIO": [126.25, 931.25, 531.25]
                }
            },

            "CANALINO VERTICALE": {
                "cuts_quantity": 2,
                "cuts_length": 1970,
                "l_angle": 45,
                "r_angle": 45,
            },

            "CANALINO ORIZZONTALE": {
                "cuts_quantity": 2,
                "cuts_length": 760,
                "l_angle": 45,
                "r_angle": 45,
            },

            "MONTANTE SX": {
                "cuts_quantity": 1,
                "cuts_length": 2000,
                "l_angle": 90,
                "r_angle": 45,
            },

            "TRAVERSO SUPERIORE": {
                "cuts_quantity": 1,
                "cuts_length": 804,
                "l_angle": 45,
                "r_angle": 90,
            },

            "MONTANTE DX": {
                "cuts_quantity": 1,
                "cuts_length": 2000,
                "l_angle": 45,
                "r_angle": 45,
            },

            "PROFILO SOGLIA": {
                "cuts_quantity": 1,
                "cuts_length": 804,
                "l_angle": 90,
                "r_angle": 90
            }
        }

    def test_model_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            workbook, model = self.__close_workflow.model_definition(src, None)

            self.assertEqual(model.name, "CLOSE")
            self.assertEqual(model.width, 100)
            self.assertEqual(model.height, 80)

    def test_check_profiles(self):
        source = XlsmSource(self.__test_files["product_worksheet"])
        checked_profiles = []

        with source.open() as src:
            _, model = self.__close_workflow.profiles_definition(
                *self.__close_workflow.model_definition(src, None)
            )

            profiles = list(self.__profile_config.keys())
            for code in model.profiles:
                self.assertIn(code, profiles)
                checked_profiles.append(code)

            self.assertEqual(checked_profiles, profiles)

    def test_bars_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__close_workflow.bars_definition(
                *self.__close_workflow.profiles_definition(
                    *self.__close_workflow.model_definition(src, None)
                )
            )

            for profile_name in self.__profile_config:
                profile_configuration = self.__profile_config[profile_name]
                bars = model.profiles[profile_name].bars

                total_cuts = sum([len(bar.cuts) for bar in bars])
                self.assertEqual(total_cuts, profile_configuration["cuts_quantity"])

                cut_length = profile_configuration["cuts_length"]
                for bar in bars:
                    for cut in bar.cuts:
                        self.assertEqual(cut.length, cut_length)

                    self.assertLessEqual(sum([cut.length for cut in bar.cuts]), bar.length)

                total_cut_length = sum([cut.length for bar in bars for cut in bar.cuts])
                self.assertEqual(total_cut_length, cut_length * total_cuts)

    def test_machining_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__close_workflow.machining_definition(
                *self.__close_workflow.bars_definition(
                    *self.__close_workflow.profiles_definition(
                        *self.__close_workflow.model_definition(src, None)
                    )
                )
            )

        for profile_name in self.__profile_config:
            profile_configuration = self.__profile_config[profile_name]
            profile = model.profiles[profile_name]

            for machining in profile.machinings:
                self.assertIn(machining.code, profile_configuration["machinings"])
                self.assertIn(machining.offset, profile_configuration["machinings"][machining.code])


