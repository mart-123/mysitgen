import unittest
from node_converter import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HtmlNode


class TestTextToHtml(unittest.TestCase):

    def test_text_to_html_normal(self):
        test_normal = TextNode('normal text', TextType.NORMAL, None)
        new_html_node: HtmlNode = text_node_to_html_node(test_normal)
        self.assertEqual(new_html_node.tag, '')
        self.assertEqual(new_html_node.value, 'normal text')

    def test_text_to_html_bold(self):
        test_bold = TextNode('bold text', TextType.BOLD, None)
        new_html_node = text_node_to_html_node(test_bold)
        self.assertEqual(new_html_node.tag, 'b')
        self.assertEqual(new_html_node.value, 'bold text')

    def test_text_to_html_italic(self):
        test_italic = TextNode('italic text', TextType.ITALIC, None)
        new_html_node = text_node_to_html_node(test_italic)
        self.assertEqual(new_html_node.tag, 'i')
        self.assertEqual(new_html_node.value, 'italic text')

    def test_text_to_html_code(self):
        test_code = TextNode('code text', TextType.CODE, None)
        new_html_node = text_node_to_html_node(test_code)
        self.assertEqual(new_html_node.tag, 'code')
        self.assertEqual(new_html_node.value, 'code text')

    def test_text_to_html_link(self):
        test_link = TextNode('link text', TextType.LINK, "https://news.bbc.co.uk")
        new_html_node = text_node_to_html_node(test_link)
        self.assertEqual(new_html_node.tag, 'a')
        self.assertEqual(new_html_node.props['href'], 'https://news.bbc.co.uk')

    def test_text_to_html_image(self):
        test_image = TextNode('image text', TextType.IMAGE, "https://images.bbc.co.uk/123")
        new_html_node = text_node_to_html_node(test_image)
        self.assertEqual(new_html_node.tag, 'img')
        self.assertEqual(new_html_node.props['src'], "https://images.bbc.co.uk/123")
        self.assertEqual(new_html_node.props['alt'], 'image text')

    def normal_empty(self):
        test_normal = TextNode('', TextType.NORMAL, None)
        new_html_node: HtmlNode = text_node_to_html_node(test_normal)
        self.assertEqual(new_html_node.tag, '')
        self.assertEqual(new_html_node.value, '')

    def bold_empty(self):
        test_bold = TextNode('', TextType.BOLD, None)
        new_html_node = text_node_to_html_node(test_bold)
        self.assertEqual(new_html_node.tag, 'b')
        self.assertEqual(new_html_node.value, '')

    def italic_empty(self):
        test_italic = TextNode('', TextType.ITALIC, None)
        new_html_node = text_node_to_html_node(test_italic)
        self.assertEqual(new_html_node.tag, 'i')
        self.assertEqual(new_html_node.value, '')

    def code_empty(self):
        test_code = TextNode('', TextType.CODE, None)
        new_html_node = text_node_to_html_node(test_code)
        self.assertEqual(new_html_node.tag, 'code')
        self.assertEqual(new_html_node.value, '')

    def link_empty(self):
        test_link = TextNode('', TextType.LINK, "")
        new_html_node = text_node_to_html_node(test_link)
        self.assertEqual(new_html_node.tag, 'a')
        self.assertEqual(new_html_node.props['href'], '')

    def image_empty(self):
        test_image = TextNode('', TextType.IMAGE, "")
        new_html_node = text_node_to_html_node(test_image)
        self.assertEqual(new_html_node.tag, 'img')
        self.assertEqual(new_html_node.props['src'], "")
        self.assertEqual(new_html_node.props['alt'], '')


if __name__ == '__main__':
    unittest.main()