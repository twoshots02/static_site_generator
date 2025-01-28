import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_children(self):
        node = LeafNode("a", "This is a link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.children, ())
        with self.assertRaises(AttributeError):
            node.children = "This is a link"

    def test_to_html(self):
        node = LeafNode("a", "This is a link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">This is a link</a>')

    def test_to_html_no_value(self):
        node = LeafNode("a", None, props={"href": "https://www.boot.dev"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a link", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), 'This is a link')

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode("div", [
            LeafNode("a", "This is a link", props={"href": "https://www.boot.dev"}),
            LeafNode("img", None, props={"src": "https://www.boot.dev/logo.png"})
        ])
        self.assertEqual(node.to_html(), '<div><a href="https://www.boot.dev">This is a link</a><img src="https://www.boot.dev/logo.png"></div>')

    def test_to_html_no_tag(self):
        node = ParentNode(None, [
            LeafNode("a", "This is a link", props={"href": "https://www.boot.dev"}),
            LeafNode("img", None, props={"src": "https://www.boot.dev/logo.png"})
        ])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()