import unittest

from textnode import *
from inline import *
from splitblocks import *
from enum import Enum

class TestSplitBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_markdown = "# Heading\n\nParagraph with **bold** text.\n\n* List item 1\n* List item 2"
        blocks = markdown_to_blocks(test_markdown)
        self.assertEqual(3, len(blocks))
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Paragraph with **bold** text.")
        self.assertEqual(blocks[2], "* List item 1\n* List item 2")
        
        test_markdown = "# Heading\n\n\n\nSecond block."
        blocks = markdown_to_blocks(test_markdown)
        self.assertEqual(2, len(blocks))
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Second block.")
        
        test_markdown = "   \n# Heading  \n\n  Paragraph with spaces.    \n\n"
        blocks = markdown_to_blocks(test_markdown)
        self.assertEqual(2, len(blocks))
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Paragraph with spaces.")

        test_markdown = "This is a single block. No blank lines here."
        blocks = markdown_to_blocks(test_markdown)
        self.assertEqual(1, len(blocks))
        self.assertEqual(blocks[0], "This is a single block. No blank lines here.")
        
        test_markdown = ""
        blocks = markdown_to_blocks(test_markdown)
        self.assertEqual(blocks, [])
       
    def test_block_to_block_type(self):
        test_strings = [
            "# Level 1",
            "### Level 3",
            "###### Level 6",
            "```\ndef hello():\n    print('hi')\n```",
            "```python\nx = 1\n```",
            ">This is a quote\n>Another line\n>Third line",
            "> This is also valid",
            "* First item\n* Second item",
            "- First item\n- Second item",
            "* First\n* Second\n* Third",
            "1. First\n2. Second\n3. Third",
            "1. Solo item",
            "Just a normal paragraph",
            "Multiple lines\nIn a paragraph\nStill a paragraph"
        ]

        expected_types = [
            "heading",
            "heading",
            "heading",
            "code",
            "code",
            "quote",
            "quote",
            "unordered_list",
            "unordered_list",
            "unordered_list",
            "ordered_list",
            "ordered_list",
            "paragraph",
            "paragraph"
        ]
        for index, test_string in enumerate(test_strings):
            self.assertEqual(block_to_block_type(test_string), expected_types[index])

if __name__ == "__main__":
    unittest.main()