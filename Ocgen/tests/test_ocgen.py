import unittest

import Utils.file_utilities
from Ocgen import ocgen
from Utils import config, file_utilities



class OcgenTests(unittest.TestCase):

    def setUp(self):
        config.setup_test_config()

    def tearDown(self):
        pass

    def test_time_restriction(self):
        start = 3
        end = 8
        pitches = ocgen.get_pitches('music/ocarina.wav', start, end, 'yin')

    def test_in_bounds_lower_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 7))

    def test_in_bounds_higher_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 11))

    def test_in_bounds_too_low(self):
        self.assertFalse(ocgen.in_bounds(9, 5))

    def test_in_bounds_too_high(self):
        self.assertFalse(ocgen.in_bounds(5, 12))

    def test_format_checking(self):
        self.assertEqual("mp3", ocgen.check_format('music.mp3', 3))
        self.assertEqual("ogg", ocgen.check_format("music.ogg", 3))
        self.assertEqual("wav", ocgen.check_format("music.wav", 3))
        self.assertEqual("", ocgen.check_format("music.pdf", 3))

    def test_pitch_smoothing(self):
        pitches = [0, 0, 0, 0, 160, 162, 161, 59, 57, 58, 58, 0]
        smoothed_pitches = ocgen.smooth_pitches(pitches)
        self.assert_note_lists_equal(smoothed_pitches, [161, 58])

    def test_path_and_file_extraction(self):
        filepath = "you/have/my/bow.axe"
        path, file = Utils.file_utilities.seperate_path_and_file(filepath)
        self.assertTrue(path == "you/have/my/" and file == "bow.axe")

    def test_get_file_extension(self):
        filepath = "Hello.world"
        self.assertEqual("world", file_utilities.get_file_extension(filepath))


    def assert_note_lists_equal(self, list1, list2):
        if len(list1) != len(list2):
            self.fail("Lists are different sizes: " + str(len(list1)) + " and " + str(len(list2)))

        for index, item in enumerate(list1):
            if item != list2[index]:
                error = "Item {} is different: {} and {}".format(index, item, list2[index])
                self.fail(error)
