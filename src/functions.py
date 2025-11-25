import re
from textnode import TextNode, TextType


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
