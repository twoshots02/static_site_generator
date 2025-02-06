from textnode import *
from htmlnode import *
from inline import *
import re
from enum import Enum

def markdown_to_blocks(markdown):
    blocks = []
    raw_blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in raw_blocks if block.strip()]
    return blocks

def block_to_block_type(markdown):
    def is_ordered_list(s):
        lines = s.split("\n")
        for i, line in enumerate(lines, start=1):
            if not re.match(fr"^{i}\. ", line):
                return False
        return True

    if re.match(r"^#{1,6} ", markdown):
        return "heading"
    elif re.fullmatch(r"```.*```", markdown, re.DOTALL):
        return "code"
    elif all(re.match(r"^[-*] ", line) for line in markdown.split("\n") if line.strip()):
        return "unordered_list"
    elif all(re.match(r"^[>]", line) for line in markdown.split("\n") if line.strip()):
        return "quote"
    elif is_ordered_list(markdown):
        return "ordered_list"
    else:
        return "paragraph"

def markdown_to_html_node(markdown):
    # Create parent div
    parent_node = ParentNode("div", [], None)
    
    # Split into blocks
    blocks = markdown_to_blocks(markdown)
    
    def count_leading_chars(s, char):
        count = 0
        for c in s:
            if c == char:
                count += 1
            else:
                break
        return count


    # Process each block
    for block in blocks:
        block_type = block_to_block_type(block)
        
        # Convert the block's text to TextNodes
        text_nodes = text_to_textnodes(block)
        
        # Now we need to create appropriate HTMLNodes based on block_type
        if block_type == "paragraph":
            # Create a p node with text_nodes as children
            block_node = ParentNode("p", [], None)
            children = []
            # Need to convert text_nodes to HTMLNodes and add as children
            for text_node in text_nodes:
                text_leaf = text_node_to_html_node(text_node)
                children.append(text_leaf)
            block_node.children = children
            parent_node.children.append(block_node)
        
        elif block_type == "heading":
            head_count = count_leading_chars(block, "#")
            clean_text = block.lstrip("#").strip()
            # Create text nodes from clean text
            text_nodes = text_to_textnodes(clean_text)
            block_node = ParentNode("h" + str(head_count), [], None)
            children = []
            # Need to convert text_nodes to HTMLNodes and add as children
            for text_node in text_nodes:
                text_leaf = text_node_to_html_node(text_node)
                children.append(text_leaf)
            block_node.children = children
            parent_node.children.append(block_node)

        elif block_type == "code":
            pre_node = ParentNode("pre", [], None)
            code_node = ParentNode("code", [], None)
            children = []
            clean_text = block.strip().strip('```').strip()
            text_nodes = text_to_textnodes(clean_text)
            # Need to convert text_nodes to HTMLNodes and add as children
            for text_node in text_nodes:                
                text_leaf = text_node_to_html_node(text_node)
                children.append(text_leaf)
            code_node.children = children
            pre_node.children.append(code_node)
            parent_node.children.append(pre_node)

        elif block_type == "quote":
            block_node = ParentNode("blockquote", [], None)
            lines = block.split('\n')
            clean_lines = [line.lstrip('>').strip() for line in lines]
            # Join back into single text
            clean_text = ' '.join(clean_lines)
            children = []
            # Need to convert text_nodes to HTMLNodes and add as children
            for text_node in text_nodes:
                text_node.text = text_node.text.lstrip("> ")
                text_leaf = text_node_to_html_node(text_node)
                children.append(text_leaf)
            block_node.children = children
            parent_node.children.append(block_node)

        elif block_type == "unordered_list":
            list_node = ParentNode("ul", [], None)
            lines = block.split("\n")
            for line in lines:
                if line.strip():
                    # Clean the line
                    clean_line = line.lstrip("*").lstrip("-").strip()
                    # Create text nodes for this line only
                    line_text_nodes = text_to_textnodes(clean_line)
                    # Create li node for this line
                    li_node = ParentNode("li", [], None)
                    # Create children list for this li_node
                    li_children = []
                    # Process text nodes for this line
                    for text_node in line_text_nodes:
                        text_leaf = text_node_to_html_node(text_node)
                        li_children.append(text_leaf)
                    li_node.children = li_children
                    list_node.children.append(li_node)
            parent_node.children.append(list_node)


        elif block_type == "ordered_list":
            list_node = ParentNode("ol", [], None)
            lines = block.split("\n")
            for line in lines:
                if line.strip():
                    # Clean the line - remove numbers, dots, and any extra spaces
                    clean_line = re.sub(r'^\d+\.', '', line).strip()
                    # Create text nodes for this line only
                    line_text_nodes = text_to_textnodes(clean_line)
                    # Create li node for this line
                    li_node = ParentNode("li", [], None)
                    # Create children list for this li_node
                    li_children = []
                    # Process text nodes for this line
                    for text_node in line_text_nodes:
                        text_leaf = text_node_to_html_node(text_node)
                        li_children.append(text_leaf)
                    li_node.children = li_children
                    list_node.children.append(li_node)
            parent_node.children.append(list_node)
    return parent_node