import unittest

import note
import tab_gen
from PIL import ImageChops


class NoteTests(unittest.TestCase):

    def test_range_compression_up(self):
        up_freqs = [880, 932, 2636, 2800]
        normal_freqs = [440, 466, 1318, 1400]

        up_notes = tab_gen.construct_notes(up_freqs, shift=1)
        normal_notes = tab_gen.construct_notes(normal_freqs)

        normal = tab_gen.construct_tabs(normal_notes)
        upshifted = tab_gen.construct_tabs(up_notes)

        self.assertTrue(equal(normal, upshifted))

    def test_range_compression_down(self):
        down_freqs = [220, 233, 659, 700]
        normal_freqs = [440, 466, 1318, 1400]

        down_notes = tab_gen.construct_notes(down_freqs, shift=-1)
        normal_notes = tab_gen.construct_notes(normal_freqs)

        normal = tab_gen.construct_tabs(normal_notes)
        downshifted = tab_gen.construct_tabs(down_notes)

        self.assertTrue(equal(normal, downshifted))

    def test_get_shift_upshift(self):
        freqs = [400, 450]
        self.assertEquals(-1, note.get_shift(freqs))

    def test_get_shift_downshift(self):
        freqs = [1350, 1400]
        self.assertEquals(1, note.get_shift(freqs))


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None

