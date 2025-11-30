import re
from enum import Enum
from textnode import TextNode, TextType
from htmlnode import ParentNode, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            # Split the text by the delimiter
            parts = node.text.split(delimiter)

            for i, part in enumerate(parts):
                # Alternate between the original text type and the new text type
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            # If not a TEXT node, keep the node as is
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all images from the node's text
        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        # Split the text by images
        remaining_text = node.text
        for alt_text, url in images:
            # Find the full image markdown syntax
            image_markdown = f"![{alt_text}]({url})"
            parts = remaining_text.split(image_markdown, 1)

            # Add the text before the image
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with the remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""

        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all links from the node's text
        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        # Split the text by links
        remaining_text = node.text
        for link_text, url in links:
            # Find the full link markdown syntax
            link_markdown = f"[{link_text}]({url})"
            parts = remaining_text.split(link_markdown, 1)

            # Add the text before the link
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            # Continue with the remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""

        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]

    # Split by bold (**) first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # Split by italic (_)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    # Split by code (`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    # Split by images
    nodes = split_nodes_image(nodes)

    # Split by links
    nodes = split_nodes_link(nodes)

    # Remove any empty TEXT nodes produced by leading/trailing delimiters
    nodes = [n for n in nodes if not (n.text_type == TextType.TEXT and n.text == "")]

    return nodes


def markdown_to_blocks(markdown):
    if markdown is None:
        return []
    # Normalize newlines (handle Windows newlines) and ensure we work with a str
    text = str(markdown).replace("\r\n", "\n").replace("\r", "\n")
    # Split on one or more blank lines (lines containing only whitespace)
    raw_blocks = re.split(r"\n\s*\n", text)
    blocks = []
    for block in raw_blocks:
        stripped = block.strip()
        if stripped:
            blocks.append(stripped)
    return blocks


def block_to_block_type(block):
    if block is None:
        return BlockType.PARAGRAPH

    lines = block.split("\n")

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def _is_ordered_list(lines):
    for index, line in enumerate(lines, start=1):
        if not re.match(rf"{index}\. ", line):
            return False
    return bool(lines)


def text_to_children(text):
    """Convert inline markdown text into a list of HTMLNode children.

    Uses `text_to_textnodes` and `text_node_to_html_node` to produce
    a list of LeafNode/HTMLNode representing inline elements.
    """
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in nodes]


def markdown_to_html_node(markdown):
    """Convert a full markdown document string into a single parent HTMLNode.

    Splits into blocks, converts each block based on its type, and returns
    a `div` ParentNode containing all block nodes.
    """
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        btype = block_to_block_type(block)

        if btype == BlockType.HEADING:
            m = re.match(r"^(#{1,6})\s(.*)$", block)
            hashes, text = m.group(1), m.group(2)
            level = len(hashes)
            children_nodes = text_to_children(text)
            children.append(ParentNode(tag=f"h{level}", children=children_nodes))

        elif btype == BlockType.PARAGRAPH:
            children_nodes = text_to_children(block)
            children.append(ParentNode(tag="p", children=children_nodes))

        elif btype == BlockType.QUOTE:
            lines = block.split("\n")
            # Remove leading '>' and optional space from each line
            inner_text = "\n".join(re.sub(r"^>\s?", "", ln) for ln in lines)
            children_nodes = text_to_children(inner_text)
            children.append(ParentNode(tag="blockquote", children=children_nodes))

        elif btype == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for ln in lines:
                # remove leading '- ' from item
                item_text = re.sub(r"^-\s", "", ln)
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            children.append(ParentNode(tag="ul", children=li_nodes))

        elif btype == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for ln in lines:
                item_text = re.sub(r"^\d+\.\s", "", ln)
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            children.append(ParentNode(tag="ol", children=li_nodes))

        elif btype == BlockType.CODE:
            # Remove the surrounding triple backticks, preserve inner as-is
            code_text = block
            if code_text.startswith("```") and code_text.endswith("```"):
                code_text = code_text[3:-3]
                # Trim a single leading/trailing newline if present
                if code_text.startswith("\n"):
                    code_text = code_text[1:]
                if code_text.endswith("\n"):
                    code_text = code_text[:-1]
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            children.append(ParentNode(tag="pre", children=[code_node]))

        else:
            # Fallback to paragraph
            children_nodes = text_to_children(block)
            children.append(ParentNode(tag="p", children=children_nodes))

    return ParentNode(tag="div", children=children)


def extract_title(markdown: str) -> str:
    """Extract the first H1 (single leading '#') from markdown.

    Returns the stripped title text. Raises ValueError if no H1 exists.
    Accepts full document markdown; finds the first line that starts with
    exactly one '#' followed by a space.
    """
    if markdown is None:
        raise ValueError("No H1 header found")

    # Normalize newlines and iterate lines
    for line in str(markdown).replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            # Strip leading/trailing whitespace from captured title
            return m.group(1).strip()
    raise ValueError("No H1 header found")
