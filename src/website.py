from textnode import *
from htmlnode import *
from inline import *
import re
from enum import Enum
from splitblocks import *
from pathlib import Path

def open_a_file(from_path, file_name):
    with open(Path(from_path) / file_name, "r") as file:
        return file.read()


def write_to_file(file_path, content):
    path = Path(file_path)
    
    # Check if the file exists
    mode = "w"  # Create and write if file doesn't exist

    with open(path, "w") as file:
        file.write(content + "\n")  # Write content with a newline

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        
        if line.startswith('#') and (len(line) == 1 or line[1] != '#'):
            return line.lstrip("#").strip()
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    markdown = open_a_file(from_path, "index.md")
    template = open_a_file(template_path, "template.html")
    root_node = markdown_to_html_node(markdown)

    content = root_node.to_html()
    title = extract_title(markdown)

    html_output = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    write_to_file(dest_path, html_output)


