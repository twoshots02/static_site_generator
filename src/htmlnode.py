from enum import Enum

VOID_ELEMENTS = ["img", "br", "hr", "input", "meta", "link"]



class HTMLNode():
    def __init__ (self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        if type(self) is not LeafNode:  # Only set children for non-LeafNodes
            self.children = children
        
        self.props = props or {}
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, props = props)
        self._children = ()

    @property
    def children(self):
        return self._children
    
    @children.setter
    def children(self, value):
        raise AttributeError("Cannot set children on a LeafNode")
    
    def to_html(self):
        # Then in LeafNode.to_html():
        if self.value is None and self.tag not in VOID_ELEMENTS:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        if self.tag in VOID_ELEMENTS:
            return f"<{self.tag}{self.props_to_html()}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
#        if children is None:
#            raise ValueError("ParentNode must have children")
        super().__init__(tag, children = children, props = props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"