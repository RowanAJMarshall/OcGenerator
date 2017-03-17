import unittest
import Ocgen

class BasicTests(unittest.TestCase):

    FILENAME = "Ocgen/tests/testdata/music.mp3"

    def setUp(self):
        Ocgen.main(FILENAME)

    def tearDown(self):
        pass

    def testFilePassedSuccessfully(self):
        upload = MusicFile(FILENAME)
        self.assertEqual(FILENAME, upload.filename)
