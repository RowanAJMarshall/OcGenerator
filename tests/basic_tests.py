import unittest

from utils import config


class BasicTests(unittest.TestCase):

    FILENAME = "Ocgen/tests/testdata/music.mp3"

    def setUp(self):
        config.setup_test_config()

    def tearDown(self):
        pass







if __name__ == '__main__':
    unittest.main()
