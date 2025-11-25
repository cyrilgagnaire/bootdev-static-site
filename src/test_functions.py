import unittest
from textnode import TextNode, TextType
from functions import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_nodes_image_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "![image1](https://example.com/img1.png) and ![image2](https://example.com/img2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/img2.png"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is text with no images", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_non_text_node(self):
        node = TextNode("Already a link", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Already a link", TextType.LINK, "https://example.com")]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_single(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.example.com"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with no links", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_non_text_node(self):
        node = TextNode(
            "Already an image", TextType.IMAGE, "https://example.com/img.png"
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Already an image", TextType.IMAGE, "https://example.com/img.png")
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes_full(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_bold_only(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_italic_only(self):
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_code_only(self):
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_image_only(self):
        text = "![image](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_link_only(self):
        text = "[link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "This is plain text with no formatting"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is plain text with no formatting", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_multiple_bold(self):
        text = "**bold1** and **bold2**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)

    # markdown_to_blocks tests
    def test_markdown_to_blocks_basic(self):
        md = "# Heading\n\nParagraph line 1.\nParagraph line 2.\n\n- item1\n- item2"
        blocks = markdown_to_blocks(md)
        expected = [
            "# Heading",
            "Paragraph line 1.\nParagraph line 2.",
            "- item1\n- item2",
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_trailing_newlines(self):
        md = "# Heading\n\nParagraph\n\n\n\n"
        blocks = markdown_to_blocks(md)
        expected = ["# Heading", "Paragraph"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_multiple_blank_lines(self):
        md = "Line 1\n\n\n\nLine 2"
        blocks = markdown_to_blocks(md)
        expected = ["Line 1", "Line 2"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_whitespace_only_blocks(self):
        md = "Line 1\n\n   \n\n\t\nLine 2"
        blocks = markdown_to_blocks(md)
        expected = ["Line 1", "Line 2"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks(None), [])

    def test_markdown_to_blocks_mixed_content(self):
        md = "# Title\n\n  Text with **bold** and _italic_.  \n\n- a\n- b  \n\nCode:\n\n`snippet`"
        blocks = markdown_to_blocks(md)
        expected = [
            "# Title",
            "Text with **bold** and _italic_.",
            "- a\n- b",
            "Code:",
            "`snippet`",
        ]
        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()
