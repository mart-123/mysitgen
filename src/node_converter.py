# module for converting text nodes into html nodes
#
from htmlnode import HtmlNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from enum import Enum

def text_node_to_html_node(text_node: TextNode):
    """ Convert text node to HTML node based on text type"""
    
    new_html_node: HtmlNode

    match text_node.text_type:
        case TextType.NORMAL:
            new_html_node = LeafNode('', text_node.text)
        case TextType.BOLD:
            new_html_node = LeafNode('b', text_node.text)
        case TextType.ITALIC:
            new_html_node = LeafNode('i', text_node.text)
        case TextType.CODE:
            new_html_node = LeafNode('code', text_node.text)
        case TextType.LINK:
            new_html_node = LeafNode('a', text_node.text, { "href": text_node.url} )
        case TextType.IMAGE:
            new_html_node = LeafNode('img', "", { "src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception(f"Cannot instantiate HtmlNode. Unrecognised TextType: {TextType.value}")

    return new_html_node

