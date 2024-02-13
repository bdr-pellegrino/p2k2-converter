import unittest
from test.data import INPUT_FILE
from p2k2_converter.core import Parser
from p2k2_converter.config import DEFAULT_CONFIG


class ParserTest(unittest.TestCase):

    def setUp(self):
        self.__expected_order_data = {
            "buyer": {
                "full_name": "Giovanni Antonioni",
                "address": "Via D.Prova, 11",
                "email": "g.ant@email.com",
                "phone": "123-4567951",
                "cell_phone": "333-4445558",
                "city": "Altrove",
            },
            "models": [
                {
                    "name": "CLOSE",
                    "width": 99.9,
                    "height": 100,
                },
                {
                    "name": "CLOSE",
                    "width": 99.9,
                    "height": 100,
                }
            ]
        }

    def test_parse(self):

        parser = Parser(workbook_path=INPUT_FILE, config_file=DEFAULT_CONFIG)
        order = parser.parse()

        # Check buyer information
        self.assertEqual(order.buyer.full_name, self.__expected_order_data["buyer"]["full_name"])
        self.assertEqual(order.buyer.address, self.__expected_order_data["buyer"]["address"])
        self.assertEqual(order.buyer.email, self.__expected_order_data["buyer"]["email"])
        self.assertEqual(order.buyer.phone, self.__expected_order_data["buyer"]["phone"])
        self.assertEqual(order.buyer.cell_phone, self.__expected_order_data["buyer"]["cell_phone"])
        self.assertEqual(order.buyer.city, self.__expected_order_data["buyer"]["city"])

        # Check model information
        self.assertEqual(len(order.models), len(self.__expected_order_data["models"]))
        for i, model in enumerate(order.models):
            self.assertEqual(model.name, self.__expected_order_data["models"][i]["name"])
            self.assertEqual(model.width, self.__expected_order_data["models"][i]["width"])
            self.assertEqual(model.height, self.__expected_order_data["models"][i]["height"])





