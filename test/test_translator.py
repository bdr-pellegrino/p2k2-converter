import unittest

from p2k2_converter.p2k2.translation import optimize_cut_distribution, p2k2_translation
from test.common import define_order


class TranslatorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        order_data = {
            "bars": {
                "PROFILE": ((3000, 1), (4000, 1))
            },
            "buyer": {
                "full_name": "Giovanni Antonioni",
                "address": "Via D.Prova, 11",
                "email": "giovanni.antonioni3@unibo.it",
                "phone": "123-4567951",
                "cell_phone": "333-4445558",
                "city": "Altrove"
            },
            "models": [
                {
                    "name": "CLOSE",
                    "width": 99.9,
                    "height": 100,
                    "profiles": [
                        {
                            "system": "TEST",
                            "code": "PROFILE",
                            "length": 100,
                            "height": 100,
                            "cuts": [
                                {
                                    "length": 3000,
                                    "height": 100,
                                    "angle_left": 90,
                                    "angle_right": 90

                                },
                                {
                                    "length": 1000,
                                    "height": 100,
                                    "angle_left": 45,
                                    "angle_right": 90
                                },
                                {
                                    "length": 2000,
                                    "height": 100,
                                    "angle_left": 90,
                                    "angle_right": 45
                                },
                            ],
                        }
                    ]
                }
            ]
        }
        cls.__available_bars, cls.__order = define_order(order_data)
        cls.__output = p2k2_translation(cls.__available_bars, cls.__order)

    def test_check_cut_distribution(self):
        bars = self.__available_bars["PROFILE"]
        cuts = self.__order.models[0].translate()["PROFILE"]
        allocations = optimize_cut_distribution(bars, cuts)

        self.assertEqual([3000, 1000], [max(cut.il, cut.ol) for cut in allocations[4000]])
        self.assertEqual([2000], [max(cut.il, cut.ol) for cut in allocations[3000]])

    def test_check_output_bars(self):
        bars_created = self.__output.body.bar
        self.assertEqual(len(bars_created), 2)
        self.assertEqual(bars_created[0].len, 4000)
        self.assertEqual(bars_created[1].len, 3000)

    def test_check_output_cuts(self):
        bars_created = self.__output.body.bar
        allocations = optimize_cut_distribution(self.__available_bars["PROFILE"],
                                                self.__order.models[0].translate()["PROFILE"])
        for bar in bars_created:
            bar_cuts = [max(cut.il, cut.ol)for cut in bar.cut]
            allocation_cuts = [max(cut.il, cut.ol) for cut in allocations[bar.len]]
            self.assertCountEqual(bar_cuts, allocation_cuts)



