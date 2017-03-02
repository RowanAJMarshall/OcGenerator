import unittest
from ocgen import ocgen
from ocgen import tab_gen
import time

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
        self.assertEqual(smoothed_pitches, [0,36,8])

if __name__ == '__main__':
    unittest.main()
