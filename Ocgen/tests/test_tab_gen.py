import unittest
from Ocgen.note import Note
from Ocgen import tab_gen


class TabGenTests(unittest.TestCase):
    

    def test_get_max_min(self):
        notes = [Note(25, 5), Note(65, 8), Note(5, 10), Note(15, 8)]
        max = 65
        min = 5
        self.assertEqual(tab_gen.get_max_min_notes(notes), (max, min))