from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "Normal"
    BOLD = "Bold"
    ITALIC = "Italic"
    CODE = "Code"
    LINKS = "Links"
    IMAGES = "Images"

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
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(tag="", value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag="img", value="",props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Invalid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: Missing closing '{delimiter}' in text: {node.text}")
        # Remove all leading empty strings
        while parts and parts[0] == "":
            parts.pop(0)

        # Remove all trailing empty strings
        while parts and parts[-1] == "":
            parts.pop(-1)

        for i, part in enumerate(parts):
            if part == "" and (i == 0 or i == len(parts)-1):
                continue
            if i % 2 == 0:
            #    print(f"Index: {i} Adding NORMAL TextNode with: {part}")
                new_nodes.append(TextNode(part, TextType.NORMAL))
            else:
            #    print(f"Index: {i} Adding {text_type} TextNode with: {part}")
                new_nodes.append(TextNode(part, text_type))

    return new_nodes