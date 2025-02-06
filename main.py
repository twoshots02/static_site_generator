from src import *
from enum import Enum
#from htmlnode import *
#from inline import *
#from splitblocks import *
import os
import shutil
import logging

# Configure logging to show the time, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def clear_destination(dest):
    """
    Deletes the destination directory if it exists and then recreates it,
    ensuring a clean copy.
    """
    if os.path.exists(dest):
        logging.info(f"Clearing destination directory: {dest}")
        shutil.rmtree(dest)
    os.makedirs(dest)
    logging.info(f"Created clean destination directory: {dest}")

def copy_recursive(src, dest):
    """
    Recursively copies contents from src to dest.
    Logs the path of each directory created and file copied.
    """
    if os.path.isdir(src):
        # Ensure the destination directory exists.
        if not os.path.exists(dest):
            os.makedirs(dest)
            logging.info(f"Created directory: {dest}")
        # Recursively copy each item in the directory.
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dest_item = os.path.join(dest, item)
            copy_recursive(src_item, dest_item)
    else:
        # Copy file and preserve metadata.
        shutil.copy2(src, dest)
        logging.info(f"Copied file: {src} -> {dest}")

if __name__ == '__main__':
    source_dir = './static'
    dest_dir = './public'
    
    # Clear destination directory to start with a clean slate.
    clear_destination(dest_dir)
    
    # Recursively copy contents from source to destination.
    copy_recursive(source_dir, dest_dir)