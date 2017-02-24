import unittest
import ocgen

class BasicTests(unittest.TestCase):

    FILENAME = "ocgen/tests/testdata/music.mp3"

    def setUp(self):
        ocgen.main(FILENAME)

    def tearDown(self):
        pass

    def testFilePassedSuccessfully(self):
        upload = MusicFile(FILENAME)
        self.assertEqual(FILENAME, upload.filename)
