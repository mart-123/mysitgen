from enum import Enum
from markdown_processor import markdown_to_blocks, text_to_textnodes, block_to_block_type
from textnode import TextNode, TextType
from markdown_processor import BlockType
from node_converter import text_node_to_html_node
from parentnode import ParentNode
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
    final_text_nodes = []

    # Transform each text block into text node(s)
    for block in markdown_blocks:
        # Get block type to determine how to transform block to text nodes
        block_type = block_to_block_type(block)

        # Transform 'code block': remove bounding ticks
        # and convert remainder to single 'text node'
        if block_type == BlockType.CODE:
            new_node = code_block_to_text_nodes(block)
            final_text_nodes.extend(new_node)
        elif block_type == BlockType.PARAGRAPH:
            new_nodes = paragraph_block_to_text_nodes(block)
            final_text_nodes.extend(new_nodes)

def code_block_to_text_nodes(block):
    new_node = TextNode(block[3:-3], TextType.CODE, None)
    return [new_node]


def paragraph_block_to_text_nodes(block):
    sub_nodes = text_to_textnodes(block)
    paragraph_node = TextNode()
    return new_nodes