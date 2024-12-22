import re
import os
from copy_directory import copy_directory

def main():
    src = "static"
    dest = "public"
    src = f"{os.getcwd()}/{src}"
    dest = f"{os.getcwd()}/{dest}"

    copy_directory(src, dest)



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
