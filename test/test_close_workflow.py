import unittest

from p2k2_converter.core.workflow.close import Close
from p2k2_converter.pipeline.source import XlsmSource


class TestCloseWorkflow(unittest.TestCase):

    def setUp(self):
        self.__test_files = {
            "data_insertion": "data/close/inserimento_dati.xlsm",
            "product_worksheet": "data/close/dummy.xlsx"
        }
        self.__close_workflow = Close()
        pass

    def test_model_definition(self):
        source = XlsmSource(self.__test_files["data_insertion"])
        with source.open() as src:
            model = self.__close_workflow.model_definition(src, None)
            self.assertEqual(model.name, "CLOSE")
            self.assertEqual(model.width, 100)
            self.assertEqual(model.height, 200)

