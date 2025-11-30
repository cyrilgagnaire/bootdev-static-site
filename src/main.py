import os
from functions import markdown_to_html_node, extract_title
from copy_static import copy_static_to_public


def main():
    # Get the project root directory (parent of src/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Define paths relative to project root
    static_path = os.path.join(project_root, "static")
    public_path = os.path.join(project_root, "public")

    # 1) Delete anything in public (handled inside copy function)
    # 2) Copy all static files from static to public
    print("Copying static files to public directory...")
    copy_static_to_public(static_path, public_path)
    print("Static copy complete!")

    # 3) Generate pages recursively from content directory
    content_dir = os.path.join(project_root, "content")
    template_html = os.path.join(project_root, "template.html")
    generate_pages_recursive(content_dir, template_html, public_path)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    """
    Recursively crawl the content directory and generate HTML pages for all markdown files.
    Maintains the same directory structure in the destination.

    Args:
        dir_path_content: Path to the content directory to crawl
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML
    """
    # Iterate through all entries in the content directory
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path):
            # If it's a markdown file, generate HTML
            if entry.endswith(".md"):
                # Convert .md extension to .html
                html_filename = entry[:-3] + ".html"
                dest_path = os.path.join(dest_dir_path, html_filename)
                generate_page(entry_path, template_path, dest_path)

        elif os.path.isdir(entry_path):
            # If it's a directory, recursively process it
            dest_subdir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(entry_path, template_path, dest_subdir)


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read markdown
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Convert markdown to HTML string
    html_root = markdown_to_html_node(md)
    html_str = html_root.to_html()

    # Extract title
    title = extract_title(md)

    # Replace placeholders
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_str)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write output
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


if __name__ == "__main__":
    main()
