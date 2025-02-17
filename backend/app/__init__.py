'''Folder inits'''
from pathlib import Path

# Get the directory where this __init__.py file is located
PACKAGE_DIR = Path(__file__).parent.absolute()

# Define DATA_DIR as a subdirectory named 'data' in the same directory as this file
DATA_DIR = PACKAGE_DIR.parent / 'data'
