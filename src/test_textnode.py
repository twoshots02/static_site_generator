import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()