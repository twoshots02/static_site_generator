from textnode import *
from htmlnode import *
import re
from enum import Enum


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

def extract_markdown_images(text):
    #text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\[\]]*)\)", text)
    return (matches)
    
    

def extract_markdown_links(text):
    #text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\[\]]*)\)", text)
    return (matches)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
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
                new_nodes.append(TextNode(new_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.LINKS, url))
            remaining_text = new_text[1] if len(new_text) > 1 else ""
        if not remaining_text and (len(links) > 1 or new_text[0]):
            new_nodes.append(TextNode("", TextType.NORMAL))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    return new_nodes
   

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
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
                new_nodes.append(TextNode(new_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.IMAGES, url))
            remaining_text = new_text[1] if len(new_text) > 1 else ""
            if remaining_text == "" and new_text[0]: new_nodes.append(TextNode("", TextType.NORMAL))
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    return new_nodes
    