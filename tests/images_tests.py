import unittest
from ocgen import ocgen
from ocgen import tab_gen
from ocgen.note import Note
import os

class BasicTests(unittest.TestCase):

    FILENAME = "ocgen/tests/testdata/music.mp3"

    def setUp(self):
       pass

    def tearDown(self):
        pass


    def test_image_construction(self):
        print(str(os.getcwd()))
        list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        tab_gen.construct_tabs(list).show()
