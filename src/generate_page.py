from markdown_to_html import markdown_to_html
from markdown_processor import extract_title
import os
import shutil

def generate_page(from_path, template_path, to_path):
    """
    Converts a markdown file to html, using the given template.
    """
    print(f"Generating page...\nfrom:{from_path} \nto:{to_path} \nusing: {template_path}")

    # Get source markdown
    if os.path.exists(from_path) == False:
        raise Exception(f"Source directory not found: {from_path}")

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
    html_file = open(to_path, 'w')
    html_file.write(template)
    html_file.close()



def generate_pages_recursive(from_dir, template_file, to_dir, level: int=0):
    """
    Crawls a directory and generates html page for each markdown
    document, using the given template. Calls itself recursively
    for any sub-directories.
    """
    print(f"\nRecursive page generation for markdown directory: {from_dir}\nWriting to dest: {to_dir}\n")

    # On initial call (before recursion), validate source root (must exist)
    if level == 0:
        if os.path.exists(from_dir) == False:
            raise Exception(f"\nMarkdown directory not found: {from_dir}")

    # On first-level recursion (sub-directory), remove destination (clean start)
    # if level == 1:
    #    if os.path.exists(to_dir) == True:
    #        print(f"\nDeleting old destination directory: {to_dir}")
    #        shutil.rmtree(to_dir)

    structure = os.listdir(from_dir)

    for item in structure:
        src_item = os.path.join(from_dir, item)
        dest_item = os.path.join(to_dir, item)

        if os.path.isfile(src_item):
            generate_page(src_item, template_file, dest_item)
        else:
            generate_pages_recursive(src_item, template_file, dest_item, (level + 1))

    return 0
