from enum import Enum
import re
from markdown_processor import markdown_to_blocks, text_to_text_nodes, block_to_block_type
from textnode import TextNode, TextType
from markdown_processor import BlockType
from node_converter import text_node_to_html_node
from parentnode import ParentNode
from leafnode import LeafNode
from htmlnode import HtmlNode

def markdown_to_html(markdown: str):
    """
    Converts markdown document to html document. Several stages:
        - Convert markdown document to blocks
        - Transform each block to text node(s)
        - Convert text nodes to html nodes
        - Combine html nodes into html document
    """
    # Split markdown into 'blocks' (delineated by blank lines)
    markdown_blocks: list[str] = markdown_to_blocks(markdown)
    final_html_nodes = []

    # Transform each text block into html parent node with >= 1 child nodes
    for block in markdown_blocks:
        # Get block type to determine how to transform block
        block_type = block_to_block_type(block)

        # Convert text block to html parent/children
        if block_type == BlockType.CODE:
            new_node = code_block_to_html(block)
            final_html_nodes.append(new_node)
        elif block_type == BlockType.PARAGRAPH:
            new_node = paragraph_block_to_html(block)
            final_html_nodes.append(new_node)
        elif block_type == BlockType.QUOTE:
            new_node = quote_block_to_html(block)
            final_html_nodes.append(new_node)
        elif block_type == BlockType.UNORDERED_LIST:
            new_node = unordered_list_block_to_html(block)
            final_html_nodes.append(new_node)
        elif block_type == BlockType.ORDERED_LIST:
            new_node = ordered_list_block_to_html(block)
            final_html_nodes.append(new_node)

        # Return HTML 'ol' parent node containing 'li' child nodes
    div_html_node = ParentNode('div', final_html_nodes, None)

    return div_html_node


def code_block_to_html(block):
    """
    Converts code block to <pre> html node containing 'code' node.
    Helper function for markdown_to_html.
    """
    # remove enclosing triple ticks and convert to 'code' text node
    text_node: TextNode = TextNode(block[3:-3], TextType.CODE, None)

    # convert to 'code' html node
    html_node: LeafNode = text_node_to_html_node(text_node)

    # embed in 'pre' html node
    pre_html_node = ParentNode('pre', [html_node], None)

    return pre_html_node



def paragraph_block_to_html(block):
    """
    Converts paragraph block to '<p>' html node containing text and
    various embedded nodes such as bold, italic, code, link, image.
    Helper function for markdown_to_html.
    """
    # Split block into text nodes of various embedded types (italic, bold, code, link, etc)
    text_nodes = text_to_text_nodes(block)
    # Convert text nodes to html nodes
    html_nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    # Enclose new html nodes in a <p> node
    paragraph_html_node = ParentNode('p', html_nodes, None)

    return paragraph_html_node



def quote_block_to_html(block):
    """
    Converts quote block to '<blockquote>' html node containing text.
    Helper function for markdown_to_html.
    """
    stripped_lines = []

    # Remove '>' from beginning of each line of quote block
    for line in block.split("\n"):
        stripped_lines.append(line[1:])

    # Reconstitute the quote block without the '>' prefixes    
    quote_text = '\n'.join(stripped_lines)

    # Return html leaf node for the block quote
    quote_html_node = LeafNode('blockquote', quote_text, None)

    return quote_html_node



def unordered_list_block_to_html(block):
    """
    Converts unordered list block to '<ul>' html node containing '<li>' nodes.
    Note the markdown may involve '*' or '-' prefixes; function works for both.
    Helper function for markdown_to_html.
    """
    list_items: list[LeafNode] = []

    # For each list item, remove '* ' or '- ' prefix and create html leaf node
    for line in block.split('\n'):
        list_items.append(LeafNode('li', line[2:], None))

    # Return HTML 'ul' parent node containing 'li' child nodes
    ul_html_node = ParentNode('ul', list_items, None)

    return ul_html_node



def ordered_list_block_to_html(block):
    """
    Converts ordered list block to '<ol>' html node containing '<li>' nodes.
    Helper function for markdown_to_html.
    """
    list_items: list[LeafNode] = []

    # For each list item, remove 'n. ' prefix and create html leaf node
    for line in block.split('\n'):
        after_prefix = re.match("[0-9]*. ", line[0:]).end(0)
        list_item = LeafNode('li', line[after_prefix:], None)
        list_items.append(list_item)

    # Return HTML 'ol' parent node containing 'li' child nodes
    ol_html_node = ParentNode('ol', list_items, None)

    return ol_html_node


