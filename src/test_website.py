import unittest

from textnode import *
from inline import *
from splitblocks import *
from enum import Enum


import unittest
from website import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_h1(self):
        self.assertEqual(extract_title("# Hello World"), "Hello World")
    
    def test_h1_with_whitespace(self):
        self.assertEqual(extract_title("#      Spacey     "), "Spacey")
    
    def test_multiple_headers(self):
        markdown = "## Not this\n# Yes this\n### Not this"
        self.assertEqual(extract_title(markdown), "Yes this")
    
    def test_h1_in_middle(self):
        markdown = "some text\n# The Title\nmore text"
        self.assertEqual(extract_title(markdown), "The Title")
    
    def test_no_h1_raises_exception(self):
        markdown = "## No H1 here\n### Still no H1"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header found")

if __name__ == '__main__':
    unittest.main()