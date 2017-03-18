import unittest

from Ocgen import ocgen
from utils import config


class OcgenTests(unittest.TestCase):

    def setUp(self):
        config.setup_test_config()

    def tearDown(self):
        pass

    def test_in_bounds_lower_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 7))

    def test_in_bounds_higher_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 11))

    def test_in_bounds_too_low(self):
        self.assertFalse(ocgen.in_bounds(9, 5))

    def test_in_bounds_too_high(self):
        self.assertFalse(ocgen.in_bounds(5, 12))

    def test_format_checking(self):
        self.assertEqual("mp3", ocgen.check_format('music.mp3'))
        self.assertEqual("ogg", ocgen.check_format("music.ogg"))
        self.assertEqual("wav", ocgen.check_format("music.wav"))
        self.assertEqual("", ocgen.check_format("music.pdf"))

    def test_pitch_smoothing(self):
        pitches = [0, 0, 0, 0, 35, 35, 37, 9, 7, 8, 8, 0]
        smoothed_pitches = ocgen.smooth_pitches(pitches)
        self.assert_note_lists_equal(smoothed_pitches, [36, 8])

    def assert_note_lists_equal(self, list1, list2):
        if len(list1) != len(list2):
            self.fail("Lists are different sizes: " + str(len(list1)) + " and " + str(len(list2)))

        for index, item in enumerate(list1):
            if item != list2[index]:
                error = "Item {} is different: {} and {}, {} and {}".format(index, item.pitch, list2[index].pitch, item.pitch_num, list2[index].pitch_num)
                self.fail(error)