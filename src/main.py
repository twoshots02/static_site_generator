from textnode import *
from enum import Enum
from htmlnode import *
from inline import *


def main():
#    text_node = TextNode("This is a text node", TextType.BOLD.value, "https://www.boot.dev")
#    print(f"TextNode({text_node.text}, {text_node.text_type}, {text_node.url})")
#    print(text_node.text)
#    print(text_node.text_type)
#    print(text_node.url)
#    delimiter_node3 = TextNode("** **bold** **", TextType.NORMAL)
#    result3 = split_nodes_delimiter([delimiter_node3], "**", TextType.BOLD)
#    print(f"the results are: {result3}")
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    extract_markdown_links(text)

main()