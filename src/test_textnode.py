import unittest

from textnode import TextNode, TextType, text_node_to_html_node

from enum import Enum

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node4)

    def test_str(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node), "This is a text node (TextType.BOLD)")

        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(str(node2), "This is a text node (TextType.NORMAL)")    
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "This is a text node (TextType.BOLD)")

        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(repr(node2), "This is a text node (TextType.NORMAL)")

    def test_text_node_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

        text_node2 = TextNode("This is a text node", TextType.NORMAL)
        html_node2 = text_node_to_html_node(text_node2)
        self.assertEqual(html_node2.tag, "")
        self.assertEqual(html_node2.value, "This is a text node")

        text_node3 = TextNode("This is a text node", TextType.ITALIC)
        html_node3 = text_node_to_html_node(text_node3)
        self.assertEqual(html_node3.tag, "i")
        self.assertEqual(html_node3.value, "This is a text node")

        text_node4 = TextNode("This is a text node", TextType.CODE)
        html_node4 = text_node_to_html_node(text_node4)
        self.assertEqual(html_node4.tag, "code")
        self.assertEqual(html_node4.value, "This is a text node")

        text_node5 = TextNode("This is a text node", TextType.LINKS, "https://www.boot.dev")
        html_node5 = text_node_to_html_node(text_node5)
        self.assertEqual(html_node5.tag, "a")
        self.assertEqual(html_node5.value, "This is a text node")
        self.assertEqual(html_node5.props, {"href": "https://www.boot.dev"})

        text_node6 = TextNode("This is a text node", TextType.IMAGES, "https://www.boot.dev")
        html_node6 = text_node_to_html_node(text_node6)
        self.assertEqual(html_node6.tag, "img")
        self.assertEqual(html_node6.value, "")
        self.assertEqual(html_node6.props, {"src": "https://www.boot.dev", "alt": "This is a text node"})

        with self.assertRaises(ValueError):
            html_node7 = text_node_to_html_node("not a text node")
        


if __name__ == "__main__":
    unittest.main()