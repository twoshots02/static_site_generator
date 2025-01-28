

class HTMLNode():
    def __init__ (self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        if type(self) is not LeafNode:  # Only set children for non-LeafNodes
            self.children = children or []
        
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
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

