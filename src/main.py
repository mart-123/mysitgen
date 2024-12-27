import re
import os
from generate_page import generate_page
from copy_directory import copy_directory

def main():
    """
    Main controlling logic for markdown->html converter.

    Steps:
        - Directory copy: 'static' to 'public'
        - Convert md document (root dir) to html ('public' dir)
    """
    copy_src = "static"
    copy_dest = "public"
    
    copy_src = f"{os.getcwd()}/{copy_src}"
    copy_dest = f"{os.getcwd()}/{copy_dest}"
    copy_directory(copy_src, copy_dest)

    gen_src = "content/index.md"
    gen_dest = "public/index.html"
    gen_template = "template.html"
    gen_src = f"{os.getcwd()}/{gen_src}"
    gen_dest = f"{os.getcwd()}/{gen_dest}"
    gen_template = f"{os.getcwd()}/{gen_template}"
    generate_page(gen_src, gen_template, gen_dest)



def messing_about():
#    print("no functionality in main()")
    my_str = "this is **bold1****bold2** text"
    delim = '**'
    my_list = my_str.split(delim)
#    print(my_list)

    text = "Text with images: ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    matches = re.findall(r"!\[.*?\]\(.*?\)", text)
    alt_text = matches[0].split('](')[0][2:]
    url = matches[0].split('](')[1][:-1]
    print(f"Matches: {matches}")
    print(f"alt_text: {alt_text}, url: {url}")

    if "![" in text:
        print("image embedded")

    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]


main()
