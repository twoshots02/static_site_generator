from textnode import *
from htmlnode import *
from inline import *
import re
from enum import Enum
from splitblocks import *

def open_a_file(from_path, file_name):
    with open(from_path + "/" + file_name, "r") as file:
        return file.read()

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