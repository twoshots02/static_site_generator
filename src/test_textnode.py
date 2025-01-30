import unittest

from textnode import *
from inline import *
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
        
        
    def test_split_nodes_delimiter(self):
        delimiter_node = TextNode("This is a **bold** text", TextType.NORMAL)
        result =  split_nodes_delimiter([delimiter_node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL)
        ])

        delimiter_node1 = TextNode("This has no special markup", TextType.NORMAL)
        result1 = split_nodes_delimiter([delimiter_node1], "**", TextType.BOLD)
        self.assertEqual(result1, [TextNode("This has no special markup", TextType.NORMAL)])

        delimiter_node2 = TextNode("Start **bold1** and **bold2** end", TextType.NORMAL)
        result2 = split_nodes_delimiter([delimiter_node2], "**", TextType.BOLD)
        self.assertEqual(result2, [
        TextNode("Start ", TextType.NORMAL),
        TextNode("bold1", TextType.BOLD),
        TextNode(" and ", TextType.NORMAL),
        TextNode("bold2", TextType.BOLD),
        TextNode(" end", TextType.NORMAL)
        ])

        delimiter_node3 = TextNode("** **bold** **", TextType.NORMAL)
        result3 = split_nodes_delimiter([delimiter_node3], "**", TextType.BOLD)
        self.assertEqual(result3, [
        TextNode(" ", TextType.NORMAL),
        TextNode("bold", TextType.BOLD),
        TextNode(" ", TextType.NORMAL)
        ])

        delimiter_node4 = TextNode("Here is an **unclosed bold", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([delimiter_node4], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images_result = extract_markdown_images(text)
        self.assertEqual(images_result, [("rick roll",
                                          "https://i.imgur.com/aKaOqIh.gif"),
                                          ("obi wan",
                                           "https://i.imgur.com/fJRm4Vk.jpeg"
                                        )])
    def extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links_result = extract_markdown_links(text)
        self.assertEqual(links_result, 
                        [("to boot dev",
                           "https://www.boot.dev"),
                           ("to youtube",
                            "https://www.youtube.com/@bootdotdev"
                        )])
if __name__ == "__main__":
    unittest.main()