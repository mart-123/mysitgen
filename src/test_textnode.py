import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This node should have null url", TextType.IMAGE, None)
        node2 = TextNode("This node should have null url", TextType.IMAGE)
        self.assertEqual(node, node2)
    
    def test_ne_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)
    
    def test_ne_url(self):
        node = TextNode("Another node", TextType.ITALIC, "https:\\blab")
        node2 = TextNode("Another node", TextType.ITALIC, "https:\\blab ")
        self.assertNotEqual(node, node2)
    


if __name__ == "__main__":
    unittest.main()

