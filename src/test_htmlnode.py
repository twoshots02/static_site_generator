import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={
            "href": "https://www.boot.dev",
            "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

if __name__ == "__main__":
    unittest.main()