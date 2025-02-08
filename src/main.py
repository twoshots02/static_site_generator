from enum import Enum
from htmlnode import *
from inline import *
from splitblocks import *
from website import *
from pathlib import Path
from shutil import rmtree
import logging
import sys

# Configure logging to show the time, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

if __name__ == '__main__':
    source_dir = Path('./content')       # This is your markdown source directory
    dest_dir = Path('./public')          # This is where your HTML files will be generated
    template_file = Path('./template.html') # Path to your HTML template

    # Clear destination directory
    if dest_dir.exists():
        logging.info(f"Clearing destination directory: {dest_dir}")
        rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Check for required files and directories
    if not source_dir.exists():
        logging.error(f"Source directory not found: {source_dir}")
        sys.exit(1)  # Exit with error code if source directory is missing
    if not template_file.exists():
        logging.error(f"Template file not found: {template_file}")
        sys.exit(1)  # Exit with error code if template file is missing

    # Generate pages recursively using content and template
    logging.info(f"Generating pages with content: {source_dir}, template: {template_file}, destination: {dest_dir}")
    generate_pages_recursive(source_dir, template_file, dest_dir)

    logging.info("Page generation completed successfully.")