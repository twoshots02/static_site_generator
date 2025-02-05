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
