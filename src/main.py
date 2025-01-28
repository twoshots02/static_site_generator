from textnode import TextNode, TextType
from enum import Enum
from htmlnode import HtmlNode


def main():
    text_node = TextNode("This is a text node", TextType.BOLD.value, "https://www.boot.dev")
    print(f"TextNode({text_node.text}, {text_node.text_type}, {text_node.url})")
    print(text_node.text)
    print(text_node.text_type)
    print(text_node.url)

main()