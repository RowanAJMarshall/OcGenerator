import unittest
from ocgen import ocgen

class BasicTests(unittest.TestCase):

    FILENAME = "ocgen/tests/testdata/music.mp3"

    def setUp(self):
        ocgen.main(self.FILENAME)

    def tearDown(self):
        pass

    def testFilePassedSuccessfully(self):
        upload = ocgen.MusicFile(self.FILENAME)
        self.assertEqual(self.FILENAME, upload.filename)
        print("Hello")

print("Hello World!")
if __name__ == '__main__':
    unittest.main()
