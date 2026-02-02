import unittest

from main import extract_title


class TestBlockConversion(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# This is a title"), "This is a title")
        self.assertEqual(
            extract_title("# This is a title\nThis is a paragraph"), "This is a title"
        )
        try:
            extract_title("## This is a title\nThis is a paragraph")
        except Exception as e:
            self.assertEqual(str(e), "No title found")
        try:
            extract_title("This is a paragraph")
        except Exception as e:
            self.assertEqual(str(e), "No title found")
