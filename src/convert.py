from textnode import TextType
from htmlnode import LeafNode

def text_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text, props=None)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text, props=None ) 
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text, props=None)
        elif text_node.text_type == TextType.CODE:
            return LeafNode(tag="code", value=text_node.text, props=None)
        elif text_node.text_type == TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        else:
            raise Exception 
        

