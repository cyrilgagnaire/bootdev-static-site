from textnode import TextNode
from htmlnode import HTMLNode


def main():
    # text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(text_node.__repr__())

    html_node = HTMLNode(
        tag="p",
        value="This is a p tag",
        children="",
        props="""{"href": "https://www.google.com", "target": "_blank"},""",
    )
    print(html_node.props_to_html())


if __name__ == "__main__":
    main()
