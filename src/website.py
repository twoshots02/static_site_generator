from textnode import *
from htmlnode import *
from inline import *
import re
from enum import Enum
from splitblocks import *
from pathlib import Path
import os
import markdown

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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure destination directory exists
    Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
    
    # Read the template content
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    
    # Walk through the content directory
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):  # Process only markdown files
                md_path = Path(root) / file
                relative_path = md_path.relative_to(dir_path_content)
                html_path = Path(dest_dir_path) / relative_path.with_suffix(".html")
                
                # Ensure the subdirectories exist in destination
                html_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Read markdown content
                with open(md_path, 'r', encoding='utf-8') as md_file:
                    md_content = md_file.read()
                
                # Generate HTML content (basic replacement, modify as needed)
                # Convert Markdown to HTML
                root_node = markdown_to_html_node(md_content)
                
                html_body = root_node.to_html()
                # Extract title and replace in template
                try:
                    title = extract_title(md_content)
                except Exception as e:
                    print(f"Warning: Failed to extract title for {md_path}. Skipping. Error: {e}")
                    continue
                html_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_body)
                
                # Write the generated HTML file
                with open(html_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)

# Example usage:
# generate_pages_recursive("content", "template.html", "public")
