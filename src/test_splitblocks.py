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
    
    def test_markdown_to_html_node(self):
        # Test paragraph
        markdown = "This is a paragraph"
        expected = "<div><p>This is a paragraph</p></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )
        
        # Test heading
        markdown = "# Header"
        expected = "<div><h1>Header</h1></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )
        
        # Test multiple block types
        markdown = "# Header\n\nParagraph\n\n> Quote"
        expected = "<div><h1>Header</h1><p>Paragraph</p><blockquote>Quote</blockquote></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )
        
        # Test lists
        markdown = "* Item 1\n* Item 2"
        expected = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )
        
        markdown = "1. Item 1\n2. Item 2"
        expected = "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )
        
        # Test code block
        markdown = "```\ncode block\n```"
        expected = "<div><pre><code>code block</code></pre></div>"
        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            expected
        )

    def test_bold_transformation(self):
        markdown_input = "**I like Tolkien**"
        expected_output = "<b>I like Tolkien</b>"
        # Assuming markdown_to_html_node(markdown).to_html()
        # is the process that converts markdown to HTML
        html_node = markdown_to_html_node(markdown_input)
        actual_output = html_node.to_html()
        self.assertEqual(actual_output.strip(), expected_output)

    def test_link_parsing(self):
        # Given: A markdown string containing a link
        markdown_input = "[first post here](/majesty) (sorry the link doesn't work yet)"
        
        
        # Expected: Correctly parsed HTML output for the link
        expected_html_output = '<a href="/majesty">first post here</a> (sorry the link doesn\'t work yet)'
        
        # When: Calling the markdown_to_html_node and converting to HTML
        # Assuming you have a parsing function similar to this in your code
        html_node = markdown_to_html_node(markdown_input)  # Replace with your function
        actual_html_output = html_node.to_html()          # Convert node to HTML string
        
        # Then: The actual HTML should match the expected output
        self.assertEqual(actual_html_output, expected_html_output)


if __name__ == "__main__":
    unittest.main()