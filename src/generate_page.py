from markdown_to_html import markdown_to_html
from markdown_processor import extract_title
import os
import shutil

def generate_page(from_path, template_path, to_path):
    """
    Converts a markdown file to html, using the given template.
    """
    # Get source markdown
    if os.path.exists(from_path) == False:
        raise Exception(f"Source file not found: {from_path}")

    md_file = open(from_path)
    markdown = md_file.read()
    md_file.close()
    doc_title = extract_title(markdown)

    # Convert markdown to html
    html_node = markdown_to_html(markdown)
    html = html_node.to_html()

    # Open template and inject title/content
    template_file = open(template_path)
    template = template_file.read()
    template_file.close()
    template = template.replace('{{ Title }}', doc_title)
    template = template.replace('{{ Content }}', html)

    # Create destination directory if not found
    to_directory = os.path.dirname(to_path)
    if os.path.exists(to_directory) == False:
        os.makedirs(to_directory)

    # Write html to the destination file
    print(f"    Writing: {to_path}")
    html_file = open(to_path, 'w')
    html_file.write(template)
    html_file.close()



def generate_pages_recursive(from_dir, template_file, to_dir, level: int=0):
    """
    Crawls a directory and generates html page for each markdown
    document, using the given template. Calls itself recursively
    for any sub-directories.
    """
    # On initial call (before recursion), validate source root (must exist)
    if level == 0:
        if os.path.exists(from_dir) == False:
            raise Exception(f"Markdown source directory not found: {from_dir}")

    # Process source files/sub-directories
    structure = os.listdir(from_dir)

    for item in structure:
        # Build full path of source/destination
        src_item = os.path.join(from_dir, item)

        # Convert markdown file to html or recursively process sub-directory
        if os.path.isfile(src_item):
            if item.split('.')[1] == 'md':
                dest_item = os.path.join(to_dir, f"{item.split('.')[0]}.html")
                generate_page(src_item, template_file, dest_item)
        else:
            dest_item = os.path.join(to_dir, item)
            generate_pages_recursive(src_item, template_file, dest_item, (level + 1))

    return 0
