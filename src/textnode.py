from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "Text"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINK = "Link"
    IMAGE = "Image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __str__(self):
        return f"{self.text} ({self.text_type})"
    
    def __repr__(self):
        return f"{self.text} ({self.text_type})"
    
    def __eq__(self, other):   
        if isinstance(other, TextNode):
            return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
            )
        return False
    
def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("text_node must be a TextNode")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag="", value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="",props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")
    
