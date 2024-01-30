import unittest
from p2k2_converter.p2k2 import BarBuilder, CutBuilder


class BarBuilderTest(unittest.TestCase):
    def test_build_bar(self):
        bar = BarBuilder("brand", "system", "profile_code") \
            .add_length(100) \
            .add_height(100) \
            .add_bars_cut_together(1) \
            .add_cut(CutBuilder().add_right_cutting_angle(90).add_left_cutting_angle(90).add_cut_length(100).build()) \
            .build()

        self.assertEqual(bar.bran, "brand")
        self.assertEqual(bar.syst, "system")
        self.assertEqual(bar.code, "profile_code")

        self.assertEqual(bar.h, 100)
        self.assertEqual(bar.len, 100)

        self.assertEqual(bar.mlt, 1)

    def test_build_bar_without_a_cut(self):
        with self.assertRaises(ValueError):
            BarBuilder("brand", "system", "profile_code") \
                .add_length(100) \
                .add_height(100) \
                .build()

    def test_build_bar_without_length(self):
        with self.assertRaises(ValueError):
            BarBuilder("brand", "system", "profile_code") \
                .add_height(100) \
                .add_cut(CutBuilder().add_right_cutting_angle(90).add_left_cutting_angle(90).add_cut_length(100).build()) \
                .build()

    