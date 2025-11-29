import os
from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode
from functions import *
from copy_static import copy_static_to_public


def main():
    # Get the project root directory (parent of src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Define paths relative to project root
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")

    # Copy static files to public directory
    print("Copying static files to public directory...")
    copy_static_to_public(static_path, public_path)
    print("Copy complete!")

    # Original test code
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    new_nodes = split_nodes_link([node])

    print(new_nodes)


if __name__ == "__main__":
    main()
