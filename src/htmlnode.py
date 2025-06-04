class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None): 
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is not None and len(self.props) > 0:
            result = ""
            for key, value in self.props.items():
                result += f' {key}="{value}"'
            return result
        return ""
    
    def __repr__(self):
        return f"tag= {self.tag}, value= {self.value}, children= {self.children}, props= {self.props} "

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
           super().__init__(tag, value, children=None, props=props)
    def to_html(self):
         if self.value == None:
             raise ValueError
         if self.tag == None:
             return self.value
         return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("Missing tag")
        if self.children == None:
            raise ValueError("Missing children") 
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    

    