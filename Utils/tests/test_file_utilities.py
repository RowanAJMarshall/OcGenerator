import unittest
from Utils import file_utilities

class FileUtilsTest(unittest.TestCase):

    def test_generate_filename(self):
        string = "Hello World"
        hashed = "cd1144e1b687f6d586c215f09ddd1a67a8f1c0f3"
        self.assertEqual(file_utilities.generate_filename(string, 1), hashed)

    def test_get_file_extension(self):
        filename = "file.txt"
        self.assertEqual("txt", file_utilities.get_file_extension(filename))

    def test_get_file_extension_no_extension(self):
        filename = "filetxt"
        self.assertRaises(file_utilities.FileNotRecognisedError, file_utilities.get_file_extension, filename)

    def test_seperate_path_and_file(self):
        filepath = "path/filename"
        self.assertEqual(("path/", "filename"), file_utilities.seperate_path_and_file(filepath))

    def test_seperate_path_and_file_no_path(self):
        filepath = "filename"
        self.assertEqual(("", "filename"), file_utilities.seperate_path_and_file(filepath))