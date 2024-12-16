from typing import Optional, List, Dict

# Superclass for parent and leaf nodes. Should not be instantiated.
# Contains common behaviour for converting props to HTML.
class HtmlNode():
    def __init__(self, tag: Optional[str]=None, value: Optional[str]=None,
                 children: Optional[List]=None, props: Optional[Dict]=None):
        self.tag: str = tag
        self.value: str = value
        self.children: List[HtmlNode] = children
        self.props = props

    
    # this method must be overridden by child classes
    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        """
        Convert dictionary of html props to single props string
        to be included when rendering HTML node as HTML
        """
        from functools import reduce

        def append_prop(props_string, key_value_tuple):
            temp_prop_string = props_string
            temp_prop_string += f' {key_value_tuple[0]}="{key_value_tuple[1]}"'
            return temp_prop_string

        props_for_html = ""

        if self.props is None:
            props_for_html = ""
        elif len(self.props) > 0:
            prop_tuples = list(self.props.items())
            props_for_html = reduce(append_prop, prop_tuples, "")

        return props_for_html
    

    def __repr__(self):
        """
        Returns HTML node properties (tag, children, props)
        in single, compound string for display/debugging
        """
        return(f"tag: {self.tag}\n value: {self.value}\n children: {self.children}\n props: {self.props_to_html()}")
    