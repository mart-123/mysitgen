import unittest

from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_created(self):
        test_node = HtmlNode("<p>", "some paragraph content", ['<a>','<b>','<c>'], { "font":"helvetica", "colour":"11AABB"} )
        self.assertEqual(test_node.tag, "<p>")
        self.assertEqual(test_node.value, "some paragraph content")
        self.assertEqual(test_node.children[2], "<c>")
        self.assertEqual(test_node.props["font"], "helvetica")


    def test_created_empty(self):
        test_node = HtmlNode("", "", [], {} )
        self.assertEqual(test_node.tag, "")
        self.assertEqual(test_node.value, "")
        self.assertEqual(len(test_node.children), 0)
        self.assertEqual(len(test_node.props), 0)


    def test_created_none(self):
        test_node = HtmlNode(None, None, None, None )
        self.assertIsNone(test_node.tag)
        self.assertIsNone(test_node.value)
        self.assertIsNone(test_node.children)
        self.assertIsNone(test_node.props)


if __name__ == "__main__":
    unittest.main()
