import os
import shutil

def copy_directory(src, dest, level: int = 0):
    """
    Copies source directory (files and sub-directories) to destination.
    Calls itself recursively to handle sub-directories.
    """
    # on first (non-) recursion, validate source and remove destination (clean start)
    if level == 0:
        print(f"\nBulk file copy...\n    src: {src}\n    dest: {dest}")

        if os.path.exists(src) == False:
            raise Exception(f"\nSource directory not found: {src}")

        if os.path.exists(dest) == True:
            shutil.rmtree(dest)

    # create dest directory
    os.mkdir(dest)

    structure = os.listdir(src)

    for item in structure:
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isfile(src_item):
            shutil.copy(src_item, dest_item)
        else:
            copy_directory(src_item, dest_item, (level + 1))

    if level == 0:  print("    Bulk file copy complete\n")

    return 0
