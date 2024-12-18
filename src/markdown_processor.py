# Functions to parse 'normal' text nodes for normal/bold/italic/code/image/link markdown,
# generating/inserting new nodes of the appropriate types.
from textnode import TextNode, TextType
import re
from enum import Enum

class BlockType(Enum):
    """
    Denotes the type of a 'text block' (monolithic text
    to be split into text nodes)
    )
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"



def split_nodes_by_delimiter(node_list: list[TextNode], delimiter: str, type_of_split: TextType):
    """
    Detects the given markdown delimiter in a list of text nodes,
    splitting nodes into further nodes of the given type.

    Args:
        node_list (list[TextNode]) : list of text nodes to be checked
        delimiter (str) : delimiter to be detected
        type_of_split (TextType) : type for any newly created nodes

    Do not use for images/links; other functions exist for those.
    """
    new_nodes: list[TextNode] = []

    for node in node_list:
        temp_node: TextNode = node

        # split current node into new text nodes.
        # Even indexes get original text type, odds get delimited text type.
        if temp_node.text_type == TextType.NORMAL:  # REMOVE WHEN IMPLEMENTING MULTI-NESTING
            split_strings = temp_node.text.split(delimiter)

            for index, string in enumerate(split_strings):
                if index % 2 == 0: # EVENS: retain the original text type
                    new_node = TextNode(string, temp_node.text_type, None)
                    new_nodes.append(new_node)
                else:              # ODDS: the delimited text is assigned the given text type
                    new_node = TextNode(string, type_of_split, None)
                    new_nodes.append(new_node)
        else:
            new_nodes.append(temp_node)
        
    return new_nodes



def split_nodes_image(input_nodes: list[TextNode]):
    """
    Checks list of text nodes for image delimiters, replacing delimited
    text with new 'image' nodes.
    """
    new_nodes: list[TextNode] = []

    # Process every given text node
    for node in input_nodes:
        # if normal node potentially with embedded image(s), convert to series of new nodes
        if node.text_type == TextType.NORMAL and "![" in node.text:
            images = extract_markdown_images(node.text)
            text_to_split = node.text   # reduces with each iteration of following for loop

            # generate new image node and text node for each image and its PRECEDING text
            for txt, url in images:
                before_and_after = text_to_split.split(f"![{txt}]({url})", 1)
                if before_and_after[0] != "":
                    new_nodes.append(TextNode(before_and_after[0], node.text_type, None))
                new_nodes.append(TextNode(txt, TextType.IMAGE, url))
                text_to_split = before_and_after[1]     # use remaining text in next split

            # generate text node for final text fragment (if there is any)
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, node.text_type, node.url))

        # if not normal node, or no embedded image, keep original node
        else:
            if node.text != "" and node.text != None:
                new_nodes.append(node)
        
    return new_nodes



# Process list of 'normal' text nodes, generating 'image' nodes as necessary.
def split_nodes_link(input_nodes: list[TextNode]):
    """
    Checks list of text nodes for link delimiters, replacing delimited
    text with new 'link' nodes.
    """
    new_nodes: list[TextNode] = []

    # Process every given text node
    for node in input_nodes:
        # if normal node potentially with embedded link(s),
        # convert to series of new nodes.
        if node.text_type == TextType.NORMAL and "](" in node.text:
            links = extract_markdown_links(node.text)
            text_to_split = node.text   # reduces with each iteration of following for loop

            # generate new link node and text node for each link and its PRECEDING text
            for txt, url in links:
                before_and_after = text_to_split.split(f"[{txt}]({url})", 1)
                if before_and_after[0] != "":
                    new_nodes.append(TextNode(before_and_after[0], node.text_type, None))
                new_nodes.append(TextNode(txt, TextType.LINK, url))
                text_to_split = before_and_after[1]     # use remaining text in next split

            # generate text node for final text fragment (if there is any)
            if text_to_split != "":
                new_nodes.append(TextNode(text_to_split, node.text_type, node.url))

        # if not normal node, or no embedded link, keep original node
        else:
            if node.text != "" and node.text != None:
                new_nodes.append(node)
        
    return new_nodes



def extract_markdown_images(text):
    """
    Extracts images (alt text/url pairs) from single string of raw markdown.
    Helper function for split_nodes_image.
    """    
    matches: list[str] = re.findall(r"!\[.*?\]\(.*?\)", text)
    list_of_tuples = []

    for raw_match in matches:
        alt_text = raw_match.split('](')[0][2:]
        url = raw_match.split('](')[1][:-1]
        list_of_tuples.append((alt_text, url))
    
    return list_of_tuples


# function to extract images (alt text/url pairs) from raw markdown text
def extract_markdown_links(text):
    """
    Extracts links (text/url pairs) from single string of raw markdown.
    Helper function for split_nodes_link.
    """    
    matches: list[str] = re.findall(r"\[.*?\]\(.*?\)", text)
    list_of_tuples = []

    for raw_match in matches:
        alt_text = raw_match.split('](')[0][1:]
        url = raw_match.split('](')[1][:-1]
        list_of_tuples.append((alt_text, url))
    
    return list_of_tuples



def text_to_text_nodes(text):
    """
    Converts text string into a flat (no children) structure
    of normal/italic/bold/image/link nodes.
    """
    base_node = TextNode(text, TextType.NORMAL, None)
    nodes: list[TextNode] = [base_node]

    nodes = split_nodes_by_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_by_delimiter(nodes, '*', TextType.ITALIC)
    nodes = split_nodes_by_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes



def markdown_to_blocks(markdown: str):
    """
    Converts markdown document (single string) into series
    of markdown 'blocks' which can each represent:
        - heading
        - standard paragraph
        - quote
        - code
        - unordered list
        - ordered list
    """
    # normalise multiple (>2) newlines into double newlines
    normalised = re.sub(r'\n\s*\n', '\n\n', markdown)

    # split into blocks (delimited by two newlines)
    blocks: list[str] = normalised.split('\n\n')

    # omit any 'empty' blocks (generated by excess newlines)
    cleansed_blocks: list[str] = []

    for block in blocks:
        cleansed_block = block.strip()
        if cleansed_block != "":
            cleansed_blocks.append(cleansed_block)

    return cleansed_blocks



def block_to_block_type(block: str):
    """
    Identifies type of given text block (paragraph, code, header, etc).
    Does this by pattern checking leading characters.
    """
    block_type: BlockType = BlockType.PARAGRAPH

    if len(re.findall("#{1,6} ", block[0:7])) > 0:
        block_type = BlockType.HEADING

    elif block[0:3] == "```" and block[-3:len(block)] == "```":
        block_type = BlockType.CODE
    
    elif block[0] == ">":
        block_type = BlockType.QUOTE
        for line in block.split("\n"):
            if line[0] != ">": block_type = BlockType.PARAGRAPH
    
    elif block[0:2] == "* ":
        block_type = BlockType.UNORDERED_LIST
        for line in block.split("\n"):
            if line[0:2] != "* ": block_type = BlockType.PARAGRAPH
    
    elif block[0:2] == "- ":
        block_type = BlockType.UNORDERED_LIST
        for line in block.split("\n"):
            if line[0:2] != "- ": block_type = BlockType.PARAGRAPH
    
    elif re.match("[0-9]*. ", block[0:]) != None:
        block_type = BlockType.ORDERED_LIST # pre-emptive positive, to be negated in logic
        expected_num = 0

        # each line must start 'n. ' with n ascending from 1
        for line in block.split("\n"):
            # if line prefix not per convention, block is not an ordered list
            list_item_prefix = re.match("[0-9]*. ", line[0:]).group(0)
            if list_item_prefix is None:
                block_type = BlockType.PARAGRAPH

            # if line number not sequential, block is not an ordered list
            item_num = int(re.match("[0-9]*", line[0:]).group(0))
            expected_num += 1
            if item_num != expected_num:
                block_type = BlockType.PARAGRAPH
            
    return block_type       

