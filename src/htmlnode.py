import json
from textnode import TextNode, TextType


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("NotImplementedError")

    def props_to_html(self):
        if not self.props:
            return ""

        # If props is already a dictionary, use it
        if isinstance(self.props, dict):
            props_dict = self.props
        else:
            # Clean and attempt to parse props as JSON
            try:
                cleaned_props = "".join(
                    line.strip() for line in self.props.splitlines()
                )
                props_dict = json.loads(cleaned_props)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Invalid props format. Expected a JSON string."
                ) from exc

        # Convert dictionary to HTML attributes
        return " " + " ".join(f'{key}="{value}"' for key, value in props_dict.items())

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        if children is not None:
            raise ValueError("LeafNode does not allow 'children'.")
        if value is None or value == "":
            raise ValueError("All leaf nodes must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props or {})

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None or self.tag == "":
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, value=None, props=None):
        if tag is None or tag == "":
            raise ValueError("Parent node must have a tag.")
        if children is None or children == []:
            raise ValueError("Parent node must have a children.")
        super().__init__(tag, value, children, props or {})

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag is missing.")
        if not self.children:
            raise ValueError("Children is missing.")

        # Generate opening tag with props
        opening_tag = f"<{self.tag}{self.props_to_html()}>"

        # Recursively generate HTML for children
        children_html = "".join(child.to_html() for child in self.children)

        # Generate closing tag
        closing_tag = f"</{self.tag}>"

        return f"{opening_tag}{children_html}{closing_tag}"


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise TypeError("Expected a TextNode object.")

    if text_node.text_type == TextType.TEXT:
        return LeafNode(value=text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")
