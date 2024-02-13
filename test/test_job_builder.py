import unittest
from p2k2_converter.p2k2 import BarBuilder, CutBuilder, JobBuilder


class JobBuilderTest(unittest.TestCase):

    def test_build_job(self):
        job = JobBuilder().add_bar(BarBuilder("brand", "system", "profile_code") \
                                   .add_length(100) \
                                   .add_height(100) \
                                   .add_bars_cut_together(1) \
                                   .add_cut(
            CutBuilder().add_right_cutting_angle(90).add_left_cutting_angle(90).add_cut_length(100).build()) \
                                   .build()) \
            .build()

        self.assertEqual(job.ver.mj, 1)
        self.assertEqual(job.ver.mn, 0)

        self.assertEqual(job.body.bar[0].bran, "brand")
        self.assertEqual(job.body.bar[0].syst, "system")
        self.assertEqual(job.body.bar[0].code, "profile_code")

        self.assertEqual(job.body.bar[0].h, 100)
        self.assertEqual(job.body.bar[0].len, 100)

        self.assertEqual(job.body.bar[0].mlt, 1)
        self.assertEqual(job.body.bar[0].cut[0].il, 100)
