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
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links_result = extract_markdown_links(text)
        self.assertEqual(links_result, 
                        [("to boot dev",
                           "https://www.boot.dev"),
                           ("to youtube",
                            "https://www.youtube.com/@bootdotdev"
                        )])
        
    def test_split_nodes_images(self):
        # Test basic image
        node = TextNode("Hello ![alt text](https://example.com/image.png) world", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Hello ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("alt text", nodes[1].text)
        self.assertEqual(TextType.IMAGES, nodes[1].text_type)
        self.assertEqual("https://example.com/image.png", nodes[1].url)
        self.assertEqual(" world", nodes[2].text)
        self.assertEqual(TextType.NORMAL, nodes[2].text_type)
        # Test multiple images
        node = TextNode("Start ![first](image1.png) middle ![second](image2.png) end", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(5, len(nodes))
        self.assertEqual("Start ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("first", nodes[1].text)
        self.assertEqual(TextType.IMAGES, nodes[1].text_type)
        self.assertEqual("image1.png", nodes[1].url)
        self.assertEqual(" middle ", nodes[2].text)
        self.assertEqual(TextType.NORMAL, nodes[2].text_type)
        self.assertEqual("second", nodes[3].text)
        self.assertEqual(TextType.IMAGES, nodes[3].text_type)
        self.assertEqual("image2.png", nodes[3].url)
        self.assertEqual(" end", nodes[4].text)
        self.assertEqual(TextType.NORMAL, nodes[4].text_type)
        # Test image with no surrounding text
        node = TextNode("![alt text](image.png)", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("alt text", nodes[0].text)
        self.assertEqual(TextType.IMAGES, nodes[0].text_type)
        self.assertEqual("image.png", nodes[0].url)
        
        # Test mixed content
        node = TextNode("Here's a ![image](pic.png) and a [link](https://boot.dev)", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Here's a ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("image", nodes[1].text)
        self.assertEqual(TextType.IMAGES, nodes[1].text_type)
        self.assertEqual("pic.png", nodes[1].url)
        self.assertEqual(" and a [link](https://boot.dev)", nodes[2].text)
        self.assertEqual(TextType.NORMAL, nodes[2].text_type)
        
        # Test non-NORMAL nodes (should remain unchanged)
        node = TextNode("[preserved](https://boot.dev)", TextType.CODE)
        nodes = split_nodes_image([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("[preserved](https://boot.dev)", nodes[0].text)
        self.assertEqual(TextType.CODE, nodes[0].text_type)

    def test_split_nodes_links(self):
        # Test basic link
        node = TextNode("Hello [click here](https://boot.dev) world", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Hello ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("click here", nodes[1].text)
        self.assertEqual(TextType.LINKS, nodes[1].text_type)
        self.assertEqual("https://boot.dev", nodes[1].url)

        # Test multiple links
        node = TextNode("Start [first link](https://example.com) middle [second link](https://boot.dev) end", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(5, len(nodes))
        self.assertEqual("Start ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("first link", nodes[1].text)
        self.assertEqual(TextType.LINKS, nodes[1].text_type)
        self.assertEqual("https://example.com", nodes[1].url)
        self.assertEqual(" middle ", nodes[2].text)
        self.assertEqual(TextType.NORMAL, nodes[2].text_type)
        self.assertEqual("second link", nodes[3].text)
        self.assertEqual(TextType.LINKS, nodes[3].text_type)
        self.assertEqual("https://boot.dev", nodes[3].url)
        self.assertEqual(" end", nodes[4].text)
        self.assertEqual(TextType.NORMAL, nodes[4].text_type)
        # Test mixed content
        node = TextNode("Here's a ![image](pic.png) and a [link](https://boot.dev)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Here's a ![image](pic.png) and a ", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)
        self.assertEqual("link", nodes[1].text)
        self.assertEqual(TextType.LINKS, nodes[1].text_type)
        self.assertEqual("https://boot.dev", nodes[1].url)
        self.assertEqual("", nodes[2].text)
        self.assertEqual(TextType.NORMAL, nodes[2].text_type)

        
        # Test non-NORMAL nodes (should remain unchanged)
        node = TextNode("[preserved](https://boot.dev)", TextType.CODE)
        nodes = split_nodes_link([node])  # Add this line
        self.assertEqual(1, len(nodes))
        self.assertEqual("[preserved](https://boot.dev)", nodes[0].text)
        self.assertEqual(TextType.CODE, nodes[0].text_type)

    def test_split_nodes_image(self):
        # Test no images
        node = TextNode("Just plain text", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("Just plain text", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)

        # Test single image
        node = TextNode("Before ![alt](image.png) after", TextType.NORMAL)
        nodes = split_nodes_image([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Before ", nodes[0].text)
        self.assertEqual("alt", nodes[1].text)
        self.assertEqual(TextType.IMAGES, nodes[1].text_type)
        self.assertEqual("image.png", nodes[1].url)
        self.assertEqual(" after", nodes[2].text)

        # Test non-NORMAL nodes (should remain unchanged)
        node = TextNode("![preserved](image.png)", TextType.CODE)
        nodes = split_nodes_image([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("![preserved](image.png)", nodes[0].text)
        self.assertEqual(TextType.CODE, nodes[0].text_type)
        
    def test_split_nodes_link(self):
        # Test no links
        node = TextNode("Just plain text", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("Just plain text", nodes[0].text)
        self.assertEqual(TextType.NORMAL, nodes[0].text_type)

        # Test single link
        node = TextNode("Click [here](https://boot.dev) now", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(3, len(nodes))
        self.assertEqual("Click ", nodes[0].text)
        self.assertEqual("here", nodes[1].text)
        self.assertEqual(TextType.LINKS, nodes[1].text_type)
        self.assertEqual("https://boot.dev", nodes[1].url)
        self.assertEqual(" now", nodes[2].text)

        # Test multiple links
        node = TextNode("[one](url1.com) then [two](url2.com)", TextType.NORMAL)
        nodes = split_nodes_link([node])
        self.assertEqual(4, len(nodes))
        self.assertEqual("one", nodes[0].text)
        self.assertEqual("url1.com", nodes[0].url)
        self.assertEqual(" then ", nodes[1].text)
        self.assertEqual("two", nodes[2].text)
        self.assertEqual("url2.com", nodes[2].url)

        # Test non-NORMAL nodes (should remain unchanged)
        node = TextNode("[preserved](https://boot.dev)", TextType.CODE)
        nodes = split_nodes_link([node])
        self.assertEqual(1, len(nodes))
        self.assertEqual("[preserved](https://boot.dev)", nodes[0].text)
        self.assertEqual(TextType.CODE, nodes[0].text_type)
if __name__ == "__main__":
    unittest.main()