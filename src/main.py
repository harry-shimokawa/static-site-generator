import os
import shutil
from textnode import TextNode, TextType


def copy_static(src_dir, dest_dir):
    """
    Recursively copy all contents from source directory to destination directory.
    
    First deletes all contents of destination directory to ensure clean copy,
    then copies all files and subdirectories from source to destination.
    
    Args:
        src_dir (str): Path to source directory
        dest_dir (str): Path to destination directory
    """
    # First, clean the destination directory
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create the destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Copy contents recursively
    _copy_directory_contents(src_dir, dest_dir)


def _copy_directory_contents(src_dir, dest_dir):
    """
    Helper function to recursively copy directory contents.
    
    Args:
        src_dir (str): Source directory path
        dest_dir (str): Destination directory path
    """
    if not os.path.exists(src_dir):
        print(f"Source directory does not exist: {src_dir}")
        return
    
    # List all items in source directory
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(src_path):
            # Copy file
            print(f"Copying file: {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        else:
            # Create subdirectory and recursively copy its contents
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            _copy_directory_contents(src_path, dest_path)


def main():
    # Copy static files to public directory
    static_dir = "static"
    public_dir = "public"
    
    print("Starting static file copy process...")
    copy_static(static_dir, public_dir)
    print("Static file copy completed!")
    
    # Create a demo TextNode
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(f"\nDemo TextNode: {node}")


if __name__ == "__main__":
    main()