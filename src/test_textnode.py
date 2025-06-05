import unittest

from textnode import TextNode, TextType
from convert import text_to_html_node
from splitnode import split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.example.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url= "www.google.com")
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})
    def test_image(self):
        node = TextNode("image", TextType.IMAGE, url= "www.google.com")
        html_node = text_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com", "alt": "image"})
    
class TestSplitNode(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        split_node = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node[0].text, "This is text with a")
        self.assertEqual(split_node[1].text, "bolded phrase")
        self.assertEqual(split_node[2].text, "in the middle")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(len(split_node), 3)
    def test_multiple_delimiter(self):
        node = TextNode("This is text with a **bolded** phrase in the middle of **bolded phrase**", TextType.TEXT)
        split_node = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node[0].text, "This is text with a")
        self.assertEqual(split_node[1].text, "bolded")
        self.assertEqual(split_node[2].text, "phrase in the middle of")
        self.assertEqual(split_node[3].text, "bolded phrase")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[3].text_type, TextType.BOLD)
        self.assertEqual(len(split_node), 4)
    def test_start_delimiter(self):
        node = TextNode("**This is a bolded** phrase in the middle", TextType.TEXT)
        split_node = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node[0].text, "This is a bolded")
        self.assertEqual(split_node[1].text, "phrase in the middle")
        self.assertEqual(split_node[0].text_type, TextType.BOLD)
        self.assertEqual(split_node[1].text_type, TextType.TEXT)
        self.assertEqual(len(split_node), 2)
    def test_end_delimiter(self):
        node = TextNode("This is a text in the **middle**", TextType.TEXT)
        split_node = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node[0].text, "This is a text in the")
        self.assertEqual(split_node[1].text, "middle")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(len(split_node), 2)    
    def test_no_delimiter(self):
        node = TextNode("This is a text in the middle", TextType.TEXT)
        split_node = split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD)
        self.assertEqual(split_node[0].text, "This is a text in the middle")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(len(split_node), 1)
    def test_unbalanced_delimiter(self):
        node = TextNode("**This is a bolded text in the middle", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes=[node], delimiter="**", text_type=TextType.BOLD) 
        




if __name__ == "__main__":
    unittest.main()