import unittest
from textnode import TextNode, TextType
from markdown_processor import split_nodes_by_delimiter, extract_markdown_images, extract_markdown_links
from markdown_processor import split_nodes_image, split_nodes_link, extract_title
from markdown_processor import text_to_text_nodes, markdown_to_blocks, BlockType, block_to_block_type

class TestNodeSplitter(unittest.TestCase):
    def test_split_bold(self):
        node_with_bold = TextNode("This text has a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_by_delimiter([node_with_bold], '**', TextType.BOLD)
        self.assertEqual(new_nodes[0].text, "This text has a ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")


    def test_split_italic(self):
        node_with_italic = TextNode("This text has an *italic* word", TextType.NORMAL)
        new_nodes = split_nodes_by_delimiter([node_with_italic], '*', TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, "This text has an ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " word")


    def test_split_code(self):
        node_with_code = TextNode("This text has a `10 print 'hello world'` section", TextType.NORMAL)
        new_nodes = split_nodes_by_delimiter([node_with_code], '`', TextType.CODE)
        self.assertEqual(new_nodes[0].text, "This text has a ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " section")


    def test_split_all_three(self):
        node_with_bold = TextNode("This text has a **bold** word", TextType.NORMAL)
        node_with_italic = TextNode("This text has an *italic* word", TextType.NORMAL)
        node_with_code = TextNode("This text has a `10 print 'hello world'` section", TextType.NORMAL)
        test_nodes = [node_with_bold, node_with_italic, node_with_code]

        new_nodes = split_nodes_by_delimiter(test_nodes, '**', TextType.BOLD)
        new_nodes = split_nodes_by_delimiter(new_nodes, '*', TextType.ITALIC)
        new_nodes = split_nodes_by_delimiter(new_nodes, '`', TextType.CODE)

        self.assertEqual(new_nodes[0].text, "This text has a ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[3].text, "This text has an ")
        self.assertEqual(new_nodes[4].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[5].text, " word")
        self.assertEqual(new_nodes[6].text, "This text has a ")
        self.assertEqual(new_nodes[7].text_type, TextType.CODE)
        self.assertEqual(new_nodes[8].text, " section")


    def test_extract_markdown_images(self):
        text_with_images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        results = extract_markdown_images(text_with_images)
        self.assertEqual(results[0][0], "rick roll")
        self.assertEqual(results[0][1], "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(results[1][0], "obi wan")
        self.assertEqual(results[1][1], "https://i.imgur.com/fJRm4Vk.jpeg")


    def test_extract_markdown_links(self):
        text_with_links = "This with link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        results = extract_markdown_links(text_with_links)
        self.assertEqual(results[0][0], "to boot dev")
        self.assertEqual(results[0][1], "https://www.boot.dev")
        self.assertEqual(results[1][0], "to youtube")
        self.assertEqual(results[1][1], "https://www.youtube.com/@bootdotdev")


    def test_split_images1(self):
        text_with_images = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and all!"
        node_with_images = TextNode(text_with_images, TextType.NORMAL)
        nodes = [node_with_images]

        results = split_nodes_image(nodes)

        self.assertEqual(results[0].text_type, TextType.NORMAL)
        self.assertEqual(results[0].text, "This is text with a ")
        self.assertEqual(results[1].text_type, TextType.IMAGE)
        self.assertEqual(results[1].text, "rick roll")
        self.assertEqual(results[1].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(results[2].text_type, TextType.NORMAL)
        self.assertEqual(results[2].text, " and ")
        self.assertEqual(results[3].text_type, TextType.IMAGE)
        self.assertEqual(results[3].text, "obi wan")
        self.assertEqual(results[3].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(results[4].text_type, TextType.NORMAL)
        self.assertEqual(results[4].text, " and all!")



    def test_split_links1(self):
        text_with_links = "This is text with a [rick roll](https://i.imgur.com/my_test) and [obi wan](https://i.imgur.com/fJRm4Vk.html) and all!"
        node_with_links = TextNode(text_with_links, TextType.NORMAL)
        nodes = [node_with_links]

        results = split_nodes_link(nodes)

        self.assertEqual(results[0].text_type, TextType.NORMAL)
        self.assertEqual(results[0].text, "This is text with a ")
        self.assertEqual(results[1].text_type, TextType.LINK)
        self.assertEqual(results[1].text, "rick roll")
        self.assertEqual(results[1].url, "https://i.imgur.com/my_test")
        self.assertEqual(results[2].text_type, TextType.NORMAL)
        self.assertEqual(results[2].text, " and ")
        self.assertEqual(results[3].text_type, TextType.LINK)
        self.assertEqual(results[3].text, "obi wan")
        self.assertEqual(results[3].url, "https://i.imgur.com/fJRm4Vk.html")
        self.assertEqual(results[4].text_type, TextType.NORMAL)
        self.assertEqual(results[4].text, " and all!")



    def test_split_images_no_outer(self):
        text_with_images = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node_with_images = TextNode(text_with_images, TextType.NORMAL)
        nodes = [node_with_images]

        results = split_nodes_image(nodes)

        self.assertEqual(results[0].text_type, TextType.IMAGE)
        self.assertEqual(results[0].text, "rick roll")
        self.assertEqual(results[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(results[1].text_type, TextType.NORMAL)
        self.assertEqual(results[1].text, " and ")
        self.assertEqual(results[2].text_type, TextType.IMAGE)
        self.assertEqual(results[2].text, "obi wan")
        self.assertEqual(results[2].url, "https://i.imgur.com/fJRm4Vk.jpeg")



    def test_split_links_no_outer(self):
        text_with_links = "[rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node_with_links = TextNode(text_with_links, TextType.NORMAL)
        nodes = [node_with_links]

        results = split_nodes_link(nodes)

        self.assertEqual(results[0].text_type, TextType.LINK)
        self.assertEqual(results[0].text, "rick roll")
        self.assertEqual(results[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(results[1].text_type, TextType.NORMAL)
        self.assertEqual(results[1].text, " and ")
        self.assertEqual(results[2].text_type, TextType.LINK)
        self.assertEqual(results[2].text, "obi wan")
        self.assertEqual(results[2].url, "https://i.imgur.com/fJRm4Vk.jpeg")



    def test_split_images_no_fluff(self):
        text_with_images = "![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node_with_images = TextNode(text_with_images, TextType.NORMAL)
        nodes = [node_with_images]

        results = split_nodes_image(nodes)

        self.assertEqual(results[0].text_type, TextType.IMAGE)
        self.assertEqual(results[0].text, "rick roll")
        self.assertEqual(results[0].url, "https://i.imgur.com/aKaOqIh.gif")
        self.assertEqual(results[1].text_type, TextType.IMAGE)
        self.assertEqual(results[1].text, "obi wan")
        self.assertEqual(results[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")



    def test_split_links_no_fluff(self):
        text_with_links = "[rick roll](https://i.imgur.com/aKaOqIh.html)[obi wan](https://i.imgur.com/fJRm4Vk.html)"
        node_with_links = TextNode(text_with_links, TextType.NORMAL)
        nodes = [node_with_links]

        results = split_nodes_link(nodes)

        self.assertEqual(results[0].text_type, TextType.LINK)
        self.assertEqual(results[0].text, "rick roll")
        self.assertEqual(results[0].url, "https://i.imgur.com/aKaOqIh.html")
        self.assertEqual(results[1].text_type, TextType.LINK)
        self.assertEqual(results[1].text, "obi wan")
        self.assertEqual(results[1].url, "https://i.imgur.com/fJRm4Vk.html")



    def test_split_images_broken(self):
        text_with_images = "First img no bracket![rick roll]https://i.imgur.com/aKaOqIh.gif)second no square bracket![obi wan(https://i.imgur.com/fJRm4Vk.jpeg)"
        node_with_images = TextNode(text_with_images, TextType.NORMAL)
        nodes = [node_with_images]

        results = split_nodes_image(nodes)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text_type, TextType.NORMAL)
        self.assertEqual(results[0].text, "First img no bracket![rick roll]https://i.imgur.com/aKaOqIh.gif)second no square bracket![obi wan(https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(results[0].url, None)


    def test_split_links_broken(self):
        text_with_links = "First link no bracket[rick roll]https://i.imgur.com/aKaOqIh.html)second no square bracket![obi wan(https://i.imgur.com/fJRm4Vk.html)"

        node_with_links = TextNode(text_with_links, TextType.NORMAL)
        nodes = [node_with_links]

        results = split_nodes_link(nodes)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text_type, TextType.NORMAL)
        self.assertEqual(results[0].text, "First link no bracket[rick roll]https://i.imgur.com/aKaOqIh.html)second no square bracket![obi wan(https://i.imgur.com/fJRm4Vk.html)")



    def test_split_images_empty(self):
        text_with_images = "![rick roll]()![](https://i.imgur.com/fJRm4Vk.jpeg)"
        node_with_images = TextNode(text_with_images, TextType.NORMAL)
        nodes = [node_with_images]

        results = split_nodes_image(nodes)

        self.assertEqual(results[0].text_type, TextType.IMAGE)
        self.assertEqual(results[0].text, "rick roll")
        self.assertEqual(results[0].url, "")
        self.assertEqual(results[1].text_type, TextType.IMAGE)
        self.assertEqual(results[1].text, "")
        self.assertEqual(results[1].url, "https://i.imgur.com/fJRm4Vk.jpeg")



    def test_split_links_empty(self):
        text_with_links = "[](https://i.imgur.com/aKaOqIh.html)[obi wan]()"
        node_with_links = TextNode(text_with_links, TextType.NORMAL)
        nodes = [node_with_links]

        results = split_nodes_link(nodes)

        self.assertEqual(results[0].text_type, TextType.LINK)
        self.assertEqual(results[0].text, "")
        self.assertEqual(results[0].url, "https://i.imgur.com/aKaOqIh.html")
        self.assertEqual(results[1].text_type, TextType.LINK)
        self.assertEqual(results[1].text, "obi wan")
        self.assertEqual(results[1].url, "")


    def test_text_to_textnodes(self):
        base_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_text_nodes(base_text)

        self.assertEqual(text_nodes[0].text, "This is ")
        self.assertEqual(text_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[1].text, "text")
        self.assertEqual(text_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(text_nodes[2].text, " with an ")
        self.assertEqual(text_nodes[2].text_type, TextType.NORMAL)



    def test_markdown_to_blocks_boots(self):
        raw_md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = markdown_to_blocks(raw_md)

        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(blocks[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")


    def test_markdown_to_blocks_edges(self):
        raw_md = """# This is a heading  
  
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
  
     

   

* This is the first list item in a list block
* This is a list item
* This is another list item
"""

        blocks = markdown_to_blocks(raw_md)

        self.assertEqual(blocks[0], "# This is a heading")
        self.assertEqual(blocks[1], "This is a paragraph of text. It has some **bold** and *italic* words inside of it.")
        self.assertEqual(blocks[2], "* This is the first list item in a list block\n* This is a list item\n* This is another list item")



    def test_text_to_textnodes(self):
        base_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_text_nodes(base_text)

        self.assertEqual(text_nodes[0].text, "This is ")
        self.assertEqual(text_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(text_nodes[1].text, "text")
        self.assertEqual(text_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(text_nodes[2].text, " with an ")
        self.assertEqual(text_nodes[2].text_type, TextType.NORMAL)


    def test_block_to_block_type(self):
        header_1 = "# This is a H1"
        header_2 = "## This is a H2"
        header_3 = "### This is a H3"
        header_4 = "#### This is a H4"
        header_5 = "##### This is a H5"
        header_6 = "###### This is a H6"

        block_type: BlockType = block_to_block_type(header_1)
        self.assertEqual(block_type, BlockType.HEADING)
        block_type: BlockType = block_to_block_type(header_2)
        self.assertEqual(block_type, BlockType.HEADING)
        block_type: BlockType = block_to_block_type(header_3)
        self.assertEqual(block_type, BlockType.HEADING)
        block_type: BlockType = block_to_block_type(header_4)
        self.assertEqual(block_type, BlockType.HEADING)
        block_type: BlockType = block_to_block_type(header_5)
        self.assertEqual(block_type, BlockType.HEADING)
        block_type: BlockType = block_to_block_type(header_6)
        self.assertEqual(block_type, BlockType.HEADING)

        code_block = "```This is some code\nwith newlines\and ending backticks```"
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, BlockType.CODE)

        unordered_list1 = "* This is the first list item in a UL list block\n* This is a list item\n* This is another list item"
        block_type = block_to_block_type(unordered_list1)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

        unordered_list2 = "- This is the first list item in a UL list block\n- This is a list item\n- This is another list item"
        block_type = block_to_block_type(unordered_list2)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

        ordered_list = "1. This is the first list item in a UL list block\n2. This is a list item\n3. This is another list item"
        block_type = block_to_block_type(ordered_list)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)


    def test_extract_title(self):
        heading = extract_title("# main heading")
        self.assertEqual(heading, "main heading")

        heading = extract_title("# main heading#\n## secondary heading ")
        self.assertEqual(heading, "main heading#")

        heading = extract_title("\n# main heading")
        self.assertEqual(heading, "main heading")


if __name__ == "__main__":
    unittest.main()
