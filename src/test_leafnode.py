import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_create_leafnode(self):
        test_leaf = LeafNode("p", "a simple paragraph", {"font":"terminal"})
        self.assertEqual(test_leaf.tag, "p")
        self.assertEqual(test_leaf.value, "a simple paragraph")
        self.assertEqual(test_leaf.props["font"], "terminal")
        self.assertEqual(test_leaf.to_html(), '<p font="terminal">a simple paragraph</p>')

    def test_leafnode_boot1(self):
        test_leaf = LeafNode("p", "this is a paragraph of text")
        self.assertEqual(test_leaf.to_html(), "<p>this is a paragraph of text</p>")

    def test_leafnode_boot2(self):
        test_leaf = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(test_leaf.to_html(), '<a href="https://www.google.com">Click me!</a>')



if __name__ == "__main__":
    unittest.main()
    