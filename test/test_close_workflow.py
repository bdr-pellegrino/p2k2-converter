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
                "cuts_quantity": 5,
                "cuts_length": 741,
                "l_angle": 90,
                "r_angle": 90,
                "machinings": {
                    "CERNIERA FORI ANTA": [(115, 520, 920), (0, 2, 4)],
                    "FORO SCASSI TELAIO": [(126.25, 531.25, 931.25), (0, 2, 4)]
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
                "machinings": {
                    "FORO FISSAGGIO": [(75, 538), tuple([0])]
                }
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
                "machinings": {
                    "FORO FISSAGGIO": [(75, 538), tuple([0])]
                }
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
                del self.__profile_config[code]
                checked_profiles.append(code)

            self.assertEqual(checked_profiles, profiles)

    def test_cuts_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__close_workflow.cuts_definition(
                *self.__close_workflow.profiles_definition(
                    *self.__close_workflow.model_definition(src, None)
                )
            )

            for profile_name in self.__profile_config:
                profile_configuration = self.__profile_config[profile_name]
                cuts = model.profiles[profile_name].cuts

                self.assertEqual(len(cuts), profile_configuration["cuts_quantity"])

                cut_length = profile_configuration["cuts_length"]
                for cut in cuts:
                    self.assertEqual(cut.length, cut_length)

    def test_machining_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__close_workflow.machining_definition(
                *self.__close_workflow.cuts_definition(
                    *self.__close_workflow.profiles_definition(
                        *self.__close_workflow.model_definition(src, None)
                    )
                )
            )

        for profile_name in self.__profile_config:
            profile_configuration = self.__profile_config[profile_name]
            profile = model.profiles[profile_name]
            machinings = profile.machinings
            if "machinings" in profile_configuration:

                codes = list(profile_configuration["machinings"].keys())
                current_codes = sorted(set(machining.code for machining in machinings))

                self.assertEqual(current_codes, codes)

                for code, machining_configuration in profile_configuration["machinings"].items():
                    offsets = list(machining_configuration[0])
                    current_offsets = [machining.offset for machining in machinings if machining.code == code]
                    self.assertEqual(current_offsets, offsets)

    def test_translation_definition(self):
        source = XlsmSource(self.__test_files["product_worksheet"])

        with source.open() as src:
            _, model = self.__close_workflow.translation_definition(
                *self.__close_workflow.machining_definition(
                    *self.__close_workflow.cuts_definition(
                        *self.__close_workflow.profiles_definition(
                            *self.__close_workflow.model_definition(src, None)
                        )
                    )
                )
            )
        for name, cuts in model.translate().items():
            self.assertEqual(len(cuts), self.__profile_config[name]["cuts_quantity"])

            for i, cut in enumerate(cuts):
                if cut.machinings:
                    for machining in cut.machinings.machining:
                        self.assertIn(i, self.__profile_config[name]["machinings"][machining.wcode][1])
