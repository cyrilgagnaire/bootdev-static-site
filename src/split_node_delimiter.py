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
