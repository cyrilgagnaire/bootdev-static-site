import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="p")
        node2 = HTMLNode(tag="p")
        self.assertEqual(node, node2)

    def test_prop_to_html(self):
        node = HTMLNode(tag="p", props="""{"key": "value"}""")
        result = """{"key": "value"}"""
        self.assertEqual(node.props_to_html(), result)

    def test_prop_to_html_none(self):
        node = HTMLNode(tag="p", props=None)
        result = ""
        self.assertEqual(node.props_to_html(), result)
