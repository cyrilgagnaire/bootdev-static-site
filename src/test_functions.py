import unittest
from textnode import TextNode, TextType
from functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestFunctions(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is plain text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("`code1` and `code2`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_different_delimiter(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node(self):
        node = TextNode("This is a link", TextType.LINK)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is a link", TextType.LINK),
        ]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "Here is an image ![image1](https://example.com/image1.png) and another ![image2](https://example.com/image2.png)."
        )
        self.assertListEqual(
            [
                ("image1", "https://example.com/image1.png"),
                ("image2", "https://example.com/image2.png"),
            ],
            matches,
        )

    def test_extract_images_no_matches(self):
        matches = extract_markdown_images("This text has no images.")
        self.assertListEqual([], matches)

    def test_extract_images_with_empty_alt_text(self):
        matches = extract_markdown_images("![](https://example.com/image.png)")
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Here is a [link](https://example.com) in the text."
        )
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "Check out [Google](https://google.com) and [Bing](https://bing.com)."
        )
        self.assertListEqual(
            [
                ("Google", "https://google.com"),
                ("Bing", "https://bing.com"),
            ],
            matches,
        )

    def test_extract_links_no_matches(self):
        matches = extract_markdown_links("This text has no links.")
        self.assertListEqual([], matches)

    def test_extract_links_with_empty_text(self):
        matches = extract_markdown_links("[]()")
        self.assertListEqual([("", "")], matches)


if __name__ == "__main__":
    unittest.main()
