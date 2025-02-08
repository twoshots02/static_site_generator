from textnode import *
from htmlnode import *
import re
from enum import Enum


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter: Missing closing '{delimiter}' in text: {node.text}")
        parts = node.text.split(delimiter)

        # No need to remove leading or trailing empty strings entirely
        # Instead, handle them gracefully in the loop
        for i, part in enumerate(parts):
            # Only skip empty parts at the very edges
            if part == "" and (i == 0 or i == len(parts) - 1):
                continue
            if i % 2 == 0:
                # Even index means regular text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd index means bold text
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\[\]]*)\)", text)
    return (matches)
    
    

def extract_markdown_links(text):
    #text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    matches = re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
    return (matches)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in links:
            new_text = remaining_text.split(f"[{text}]({url})", 1)
            if new_text[0]:
                new_nodes.append(TextNode(new_text[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            remaining_text = new_text[1] if len(new_text) > 1 else ""
        if not remaining_text and (len(links) > 1 or new_text[0]):
            new_nodes.append(TextNode("", TextType.TEXT))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
   

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for text, url in images:
            new_text = remaining_text.split(f"![{text}]({url})", 1)
            if new_text[0] :
                new_nodes.append(TextNode(new_text[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.IMAGE, url))
            remaining_text = new_text[1] if len(new_text) > 1 else ""
            if remaining_text == "" and new_text[0]: new_nodes.append(TextNode("", TextType.TEXT))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    new_nodes = []
    new_nodes.append(TextNode(text, TextType.TEXT))
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", text_type=TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type=TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type=TextType.CODE)
    return new_nodes
