import unittest
from p2k2_converter.p2k2 import CutBuilder

class CutBuilderTest(unittest.TestCase):
    def test_build_cut(self):
        cut = CutBuilder() \
               .add_cut_length(100) \
               .add_left_cutting_angle(45) \
               .add_right_cutting_angle(45) \
               .add_left_beta_cutting_angle(45) \
               .add_right_beta_cutting_angle(45) \
               .add_left_trim_cut_length(100) \
               .add_right_trim_cut_length(100) \
               .add_left_trim_cut_angle(45) \
               .add_right_trim_cut_angle(45) \
               .build()

        self.assertEqual(cut.il, 100)
        self.assertEqual(cut.ol, 100)

        self.assertEqual(cut.angl, 45)
        self.assertEqual(cut.angr, 45)

        self.assertEqual(cut.trml, 100)
        self.assertEqual(cut.trmr, 100)

        self.assertEqual(cut.tal, 45)
        self.assertEqual(cut.tar, 45)

    def test_build_cut_with_machining(self):
        cut = CutBuilder().add_cut_length(100).add_left_cutting_angle(45).add_right_cutting_angle(45) \
               .add_machining("M1", 10).build()

        self.assertEqual(cut.machinings.machining[0].wcode, "M1")
        self.assertEqual(cut.machinings.machining[0].offset, 10)

    def test_build_without_cutting_angles(self):
        with self.assertRaises(ValueError):
            CutBuilder().add_cut_length(100).build()

    def test_build_without_cutting_lengths(self):
        with self.assertRaises(ValueError):
            CutBuilder().add_left_cutting_angle(45).add_right_cutting_angle(45).build()

    def test_add_a_number_of_label_greater_than_four(self):
        with self.assertRaises(ValueError):
            CutBuilder().add_label("label1").\
                add_label("label2").\
                add_label("label3").\
                add_label("label4").\
                add_label("label5")

