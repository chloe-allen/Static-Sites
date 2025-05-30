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
