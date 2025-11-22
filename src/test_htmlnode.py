import unittest
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    TextNode,
    TextType,
    text_node_to_html_node,
)


class TestHTMLNode(unittest.TestCase):
    ## htmlnode tests
    def test_eq(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        self.assertEqual(node, node2)

    def test_prop_to_html(self):
        node = HTMLNode(
            tag="p",
            props="""{"href": "https://www.google.com","target":"_blank"}""",
        )
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_prop_to_html_none(self):
        node = HTMLNode(tag="p", props=None)
        result = ""
        self.assertEqual(node.props_to_html(), result)

    ## leafnode tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode(
            "p",
            "Hello, world!",
            props="""{"href": "https://www.google.com","target":"_blank"}""",
        )
        self.assertEqual(
            node.to_html(),
            """<p href="https://www.google.com" target="_blank">Hello, world!</p>""",
        )

    def test_leaf_with_children(self):
        with self.assertRaises(ValueError) as context:
            LeafNode("p", "Hello, world!", "Some children")
        self.assertEqual(str(context.exception), "LeafNode does not allow 'children'.")

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError) as context:
            LeafNode(tag="p")
        self.assertEqual(str(context.exception), "All leaf nodes must have a value.")

    ## Parent node tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    ## Text Nodes
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
