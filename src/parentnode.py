from typing import Optional, List, Dict
from htmlnode import HtmlNode

# ParentNode is an HTML node with one or more child HTML nodes.
# Tag and children are mandatory; props are optional.
class ParentNode(HtmlNode):
    def __init__(self, tag: str, children: List[HtmlNode], props: Optional[Dict[str, str]]=None):
        if tag is None:
            raise ValueError("ParentNode constructor requires a tag")
        if tag == "":
            raise ValueError("ParentNode constructor requires a tag")
        if children is None:
            raise ValueError("ParentNode constructor requires children objects")
        if len(children) == 0:
            raise ValueError("ParentNode constructor requires children objects")

        super().__init__(tag, None, children, props)

    def to_html(self):
        rendered_text = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            rendered_text += child.to_html()

        rendered_text += f"</{self.tag}>"
    
        return rendered_text