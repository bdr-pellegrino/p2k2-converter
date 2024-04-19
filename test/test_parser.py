import unittest
from test.data import INPUT_FILE
from p2k2_converter.core import Parser
from p2k2_converter.config import DEFAULT_CONFIG


class ParserTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.__expected_order_data = {
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
                    "name": "MODERNA",
                    "width": 100,
                    "height": 80,
                },
                {
                    "name": "CLICK_RAPID",
                    "width": 99.9,
                    "height": 100,
                },
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
        parser = Parser(workbook_path=INPUT_FILE, config_file=DEFAULT_CONFIG)
        cls.__bars, cls.__order = parser.parse()

    def test_check_user_information(self):
        self.assertEqual(self.__order.buyer.full_name, self.__expected_order_data["buyer"]["full_name"])
        self.assertEqual(self.__order.buyer.address, self.__expected_order_data["buyer"]["address"])
        self.assertEqual(self.__order.buyer.email, self.__expected_order_data["buyer"]["email"])
        self.assertEqual(self.__order.buyer.phone, self.__expected_order_data["buyer"]["phone"])
        self.assertEqual(self.__order.buyer.cell_phone, self.__expected_order_data["buyer"]["cell_phone"])
        self.assertEqual(self.__order.buyer.city, self.__expected_order_data["buyer"]["city"])

    def test_models(self):
        self.assertEqual(len(self.__order.models), len(self.__expected_order_data["models"]))
        for i, model in enumerate(self.__order.models):
            self.assertEqual(model.name, self.__expected_order_data["models"][i]["name"])
            self.assertEqual(model.width, self.__expected_order_data["models"][i]["width"])
            self.assertEqual(model.height, self.__expected_order_data["models"][i]["height"])

    def test_bars(self):
        total_bar_length = 0
        for configs in self.__bars.values():
            for bar_config in configs.values():
                for bar_len, bar_qty in bar_config:
                    total_bar_length += bar_len * bar_qty

        total_bar_length = 0
        for model in self.__order.models:
            total_bar_length = sum(
                sum(cut.length for cut in profile.cuts) for profile in model.profiles.values()
            )

        self.assertGreaterEqual(total_bar_length, total_bar_length)




