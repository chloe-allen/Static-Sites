import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>",)

    def test_parentnode_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

if __name__ == "__main__":
    unittest.main()