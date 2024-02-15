import unittest
from p2k2_converter.p2k2 import Translator
from test.common import define_order
from p2k2_converter.p2k2.classes import Version


class TranslatorTest(unittest.TestCase):

    def setUp(self):
        self.__translator = Translator()

    def test_check_output_version(self):
        order = define_order(number_of_models=1, number_of_profiles=2, number_of_bars=2, number_of_cuts=2)
        translated_order = self.__translator.p2k2_translation(order)

        self.assertEqual(translated_order.ver, Version(mj=1, mn=0))

    def test_check_bars(self):
        order = define_order(number_of_models=1, number_of_profiles=2, number_of_bars=2, number_of_cuts=2)
        translated_order = self.__translator.p2k2_translation(order)

        self.assertEqual(len(translated_order.body.bar), 4)
        bar_codes = ["PELLEGRINO_PROF_0", "PELLEGRINO_PROF_1", "PELLEGRINO_PROF_0", "PELLEGRINO_PROF_1"]
        for bar in translated_order.body.bar:
            self.assertIn(bar.code, bar_codes)
            bar_codes.pop(bar_codes.index(bar.code))

        self.assertEqual(bar_codes, [])

    def test_check_cuts(self):
        order = define_order(number_of_models=1, number_of_profiles=2, number_of_bars=2, number_of_cuts=2)
        translated_order = self.__translator.p2k2_translation(order)

        for bar in translated_order.body.bar:
            self.assertEqual(len(bar.cut), 2)
            for cut in bar.cut:
                self.assertEqual(cut.il, 1000)
                self.assertEqual(cut.ol, 1000)
                self.assertEqual(cut.angl, 90)
                self.assertEqual(cut.angr, 90)