import unittest
from Ocgen.note import Note
from Ocgen import tab_gen


class TabGenTests(unittest.TestCase):

    def test_get_max_min(self):
        notes = [Note(25, 5), Note(65, 8), Note(5, 10), Note(15, 8)]
        max = 65
        min = 5
        self.assertEqual(tab_gen.get_max_min_notes(notes), (max, min))

    def test_get_note_box(self):
        box = tab_gen.get_note_box_12_hole(0, 0)
        real_box = (0, 0, 129, 119)
        self.assertEqual(real_box, box)

    def test_construct_notes(self):
        pitches = [440, 740, 1320, 1171]
        actual = [("A", 440, 1), ("F\#", 739.99, 10), ("E", 1318.51, 20), ("D", 1174.66, 18)]
        self.assertEqual(tab_gen.construct_notes(pitches), actual)
