import unittest
from markdown_to_html import markdown_to_html
from htmlnode import HtmlNode
from parentnode import ParentNode
import inspect

class test_markdown_to_html(unittest.TestCase):
    """
    Test cases for function 'test_markdown_to_html'
    """
    def test_simple_para_block(self):
        text = "hello world"
        html = markdown_to_html(text)

        expected = '<div><p>hello world</p></div>'
        self.assertEqual(html.to_html(), expected)


    def test_code_block(self):
        text = "```hello world\n01 print hello\n02 goto 01```"
        html = markdown_to_html(text)
        expected = '<div><pre><code>hello world\n01 print hello\n02 goto 01</code></pre></div>'
        self.assertEqual(html.to_html(), expected)


    def test_complex_para_block(self):
        text = "hi *ital* **bo** and ![imagey](not.com/im.jpg), [linky](bbc.com)"
        html: ParentNode = markdown_to_html(text)
        expected = '<div><p>hi <i>ital</i> <b>bo</b> and <img src="not.com/im.jpg" alt="imagey"></img>, <a href="bbc.com">linky</a></p></div>'
        self.assertEqual(html.to_html(), expected)


    def test_quote_block(self):
        text = ">My three-line\n>block of\n>quotiness"
        html: ParentNode = markdown_to_html(text)
        expected = '<div><blockquote>My three-line\nblock of\nquotiness</blockquote></div>'
        self.assertEqual(html.to_html(), expected)


    def test_ul_block(self):
        text = "* One thing\n* And another thing\n* and just one more thing"
        html: HtmlNode = markdown_to_html(text)
        expected = '<div><ul><li>One thing</li><li>And another thing</li><li>and just one more thing</li></ul></div>'
        self.assertEqual(html.to_html(), expected)


    def test_ol_block(self):
#        print(f"RUNNING TEST: {__name__}.{inspect.currentframe().f_code.co_name}")
        text = "1. One thing\n2. Two thing\n3. Three thing"
        html: ParentNode = markdown_to_html(text)
        expected = '<div><ol><li>One thing</li><li>Two thing</li><li>Three thing</li></ol></div>'
        self.assertEqual(html.to_html(), expected)



def print_diagnostics(html: ParentNode):
    """
    Takes parent html node and displays properties
    """
    print("*** FINAL HTML DIAGNOSTICS (WITHIN THE DIV) ***")
    print(f"***   P-NODES: {len(html.children[0].children)}")
    if html[0].children is not None: 
        print(f"***   C-NODES IN FIRST P-NODE: {len(html.children[0].children)}")

    for parent_node in html.children[0].children:
        html_node: ParentNode = parent_node
        print(f"***         PARENT TAG: {html_node.tag}")
        print(f"***         CHILDREN: {html_node.children}")
        print(f"***         PARENT AS HTML: \n{html_node.to_html()}")


if __name__ == '__main__':
    unittest.main()

