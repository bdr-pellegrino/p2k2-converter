import unittest

from p2k2_converter.core.classes import Model
from p2k2_converter.core.workflow.close import Close
from p2k2_converter.pipeline.source import XlsmSource


class TestCloseWorkflow(unittest.TestCase):

    def setUp(self):
        self.__test_files = {
            "data_insertion": "data/close/inserimento_dati.xlsm",
            "product_worksheet": "data/close/close.xlsm"
        }
        self.__close_workflow = Close()

    def test_model_definition(self):
        source = XlsmSource(self.__test_files["data_insertion"])
        with source.open() as src:
            workbook, model = self.__close_workflow.model_definition(src, None)
            self.assertEqual(model.name, "CLOSE")
            self.assertEqual(model.width, 100)
            self.assertEqual(model.height, 200)

    def test_check_profiles(self):
        profiles_name = [
            "PROFILO DOGA",
            "CANALINO VERTICALE",
            "CANALINO ORIZZONTALE",
            "MONTANTE SX",
            "TRAVERSO SUPERIORE",
            "MONTANTE DX",
            "PROFILO SOGLIA"
        ]
        source = XlsmSource(self.__test_files["product_worksheet"])
        with source.open() as src:
            _, model = self.__close_workflow.profiles_definition(src, Model("CLOSE", 100, 200))
            for profile in model.profiles:
                self.assertIn(profile.code, profiles_name)
                profiles_name.remove(profile.code)
            self.assertEqual(len(profiles_name), 0)

    def test_profiles_definition_with_refinement(self):
        source = XlsmSource(self.__test_files["product_worksheet"])
        with source.open() as src:
            src["prod CLOSE"]["CM8"] = 1.5
            _, model = self.__close_workflow.profiles_definition(src, Model("CLOSE", 100, 200))
            for profile in model.profiles:
                if profile.code == "PROFILO DOGA":
                    self.assertEqual(profile.refinement, 1.5)
                    return

            self.fail("Refinement not found")
