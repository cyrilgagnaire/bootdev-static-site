from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode


def main():
    # text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(text_node.__repr__())

    node = ParentNode(
        tag="p",
        children=[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )

    print(node.to_html())


if __name__ == "__main__":
    main()
