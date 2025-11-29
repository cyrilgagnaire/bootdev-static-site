import os
import shutil


def copy_static_to_public(source_dir="static", dest_dir="public"):
    """
    Recursively copies all contents from source directory to destination directory.
    First deletes all contents of the destination directory to ensure a clean copy.

    Args:
        source_dir: Path to the source directory (default: "static")
        dest_dir: Path to the destination directory (default: "public")
    """
    # Delete the destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.makedirs(dest_dir)

    # Recursively copy contents
    _copy_directory_contents(source_dir, dest_dir)


def _copy_directory_contents(source_dir, dest_dir):
    """
    Recursively copies all files and subdirectories from source to destination.

    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory does not exist: {source_dir}")
        return

    # List all items in the source directory
    items = os.listdir(source_dir)

    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            # Copy file
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy2(source_path, dest_path)
        elif os.path.isdir(source_path):
            # Create subdirectory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.makedirs(dest_path)
            _copy_directory_contents(source_path, dest_path)
