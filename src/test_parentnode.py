import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_created(self):
        test_leaf_1 = LeafNode("h1", "big heading", { "font":"times", "italics":"ohyes"})
        test_leaf_2 = LeafNode("p", "first paragraph", {"font":"terminal"})
        test_parent = ParentNode("div", [test_leaf_1, test_leaf_2], { "font":"courier", "colour":"00FF00"} )

        self.assertEqual(test_parent.tag, "div")
        self.assertEqual(test_parent.props["font"], "courier")
        self.assertEqual(len(test_parent.children), 2)
        self.assertEqual(test_parent.children[1].tag, "p")

    def test_nested_parents(self):
        test_leaf_1 = LeafNode("h1", "heading", { "font":"times", "italics":"ohyes"})
        test_leaf_2 = LeafNode("p", "para", {"font":"terminal"})
        test_leaf_3 = LeafNode("h2", "head2", {"font":"comic sans"})
        test_sub_parent_1 = ParentNode("sub1", [test_leaf_1], { "font":"tahoma", "colour":"FF0000"} )
        test_sub_parent_2 = ParentNode("sub2", [test_sub_parent_1, test_leaf_2], { "font":"courier", "colour":"00FF00"} )
        test_parent = ParentNode("div", [test_leaf_3, test_sub_parent_2], { "font":"courier", "colour":"0000FF"} )

        self.assertEqual(len(test_sub_parent_1.children), 1)
        self.assertEqual(len(test_sub_parent_2.children), 2)
        self.assertEqual(len(test_parent.children), 2)
        self.assertEqual(test_parent.children[0].tag, "h2")
        self.assertEqual(test_parent.children[1].children[0].children[0].tag, 'h1')
        self.assertEqual(test_parent.children[1].children[0].children[0].props['italics'], 'ohyes')
        self.assertEqual(test_parent.children[1].children[1].tag, 'p')

    def test_parent_render_boot(self):
        test_leaf_1 = LeafNode("b", "Bold text")
        test_leaf_2 = LeafNode(None, "Normal text")
        test_leaf_3 = LeafNode("i", "italic text")
        test_leaf_4 = LeafNode(None, "Normal text")
        test_parent = ParentNode("p", [test_leaf_1, test_leaf_2, test_leaf_3, test_leaf_4], )

        self.assertEqual(test_parent.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

if __name__ == "__main__":
    unittest.main()
