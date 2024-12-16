from htmlnode import HtmlNode
from typing import Optional, Dict

# Leaf Node is a final-level node with no child nodes.
class LeafNode(HtmlNode):
    """
    Lowest level HTML node with no child nodes
    """

    def __init__(self, tag: str, value: str, props: Optional[Dict[str, str]] = None):
        if value is None:
            raise ValueError("Error instantiating LeafNode: value cannot be None")

        super().__init__(tag, value, None, props)
    

    def to_html(self):
        """
        Builds HTML tag from leaf node tag/text/props
        """
        leaf_as_html = ""

        # if leaf node has no tag, render using just the value
        if self.tag is None:
            leaf_as_html = self.value
        elif self.tag == "":
            leaf_as_html = self.value
        # otherwise render the tag with any props and its value
        else:
            leaf_as_html = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
        return leaf_as_html
    