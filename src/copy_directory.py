import os
from shutil import copy, rmtree

def copy_directory(src, dest):
    src = f"{os.getcwd()}/{src}"
    dest = f"{os.getcwd()}/{dest}"

    if os.path.exists(src) == False:
        raise Exception(f"Source directory not found: {src}")
    if os.path.exists(dest) == False:
        raise Exception(f"Source directory not found: {dest}")
    
    structure = os.listdir(src)
    for item in structure:
        print(f"item: {item}")

    return 0
