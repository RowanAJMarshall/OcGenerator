import unittest

from Ocgen import InstrumentDefinitions
from Ocgen import note
from Ocgen import tab_gen


class TabGenTests(unittest.TestCase):

    def test_get_note_box(self):
        instrument = InstrumentDefinitions.TwelveHoleOcarina()
        box = instrument.get_note_box(0, 0)
        real_box = (0, 0, 129, 119)
        self.assertEqual(real_box, box)

    def test_construct_notes(self):
        instrument = InstrumentDefinitions.TwelveHoleOcarina()
        pitches = [440, 740, 1320, 1171]
        actual = [["A", 440, 1], ["F\#", 739.99, 10], ["E", 1318.51, 20], ["D", 1174.66, 18]]
        self.assertEqual(tab_gen.construct_notes(pitches, instrument.get_notes()), actual)
