import unittest
from ocgen import ocgen
from ocgen import tab_gen
from ocgen.note import Note

class BasicTests(unittest.TestCase):

    FILENAME = "ocgen/tests/testdata/music.mp3"

    def setUp(self):
       pass

    def tearDown(self):
        pass

    def testFilePassedSuccessfully(self):
        pass

    def test_image_extraction(self):
        pass
        # tab_gen.get_image_12_hole(0).show()

    def testDownsamplePitches(self):
        nums = [0,1,2,3,4,5,7,8,9]
        filtered = [0, 3, 7]
        self.assertEqual(filtered, ocgen.filter_pitches(3, nums))

    def test_in_bounds_lower_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 7))
    
    def test_in_bounds_higher_bound(self):
        self.assertTrue(ocgen.in_bounds(9, 11))

    def test_in_bounds_too_low(self):
        self.assertFalse(ocgen.in_bounds(9, 6))

    def test_in_bounds_too_high(self):
        self.assertFalse(ocgen.in_bounds(9, 12))
    
    def test_pitch_smoothing(self):
        pitches = [0,0,0,0,35,35,37,9,7,8,8]
        smoothed_pitches = ocgen.smooth_pitches(pitches, 1)
        self.assert_note_lists_equal(smoothed_pitches, [Note(0, 4),Note(36, 3),Note(8, 4)])

    def test_get_max_min(self):
        notes = [Note(25, 5), Note(65, 8), Note(5, 10), Note(15, 8)]
        max = 65
        min = 5
        self.assertEqual(tab_gen.get_max_min_notes(notes), (max, min))

    def assert_note_lists_equal(self, list1, list2):
        if len(list1) != len(list2):
            self.fail("Lists are different sizes: " + str(len(list1)) + " and " + str(len(list2)))

        for index, item in enumerate(list1):
            if item.pitch != list2[index].pitch or item.pitch_num != list2[index].pitch_num:
                error = "Item {} is different: {} and {}, {} and {}".format(index, item.pitch, list2[index].pitch, item.pitch_num, list2[index].pitch_num)
                self.fail(error)

if __name__ == '__main__':
    unittest.main()
