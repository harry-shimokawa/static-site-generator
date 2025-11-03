import os
import shutil
from textnode import TextNode, TextType
from markdown import markdown_to_html_node


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


def extract_title(markdown):
    """
    Extract the title from markdown content.
    Looks for the first h1 heading (# Title).
    
    Args:
        markdown (str): Markdown content
        
    Returns:
        str: The title text without the # symbol
        
    Raises:
        ValueError: If no h1 heading is found
    """
    lines = markdown.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
    
    raise ValueError("No h1 heading found in markdown")


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from markdown content and template.
    
    Args:
        from_path (str): Path to the markdown file
        template_path (str): Path to the HTML template
        dest_path (str): Path where the generated HTML should be saved
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title from markdown
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML to the destination
    with open(dest_path, 'w') as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages for all markdown files in a directory tree.
    
    Crawls the content directory and generates HTML pages for every markdown file found,
    maintaining the same directory structure in the destination.
    
    Args:
        dir_path_content (str): Path to the content directory to crawl
        template_path (str): Path to the HTML template file
        dest_dir_path (str): Path to the destination directory for generated HTML
    """
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    
    # Get all items in the content directory
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(item_path):
            # Check if it's a markdown file
            if item.endswith('.md'):
                # Generate the destination HTML path
                html_filename = item.replace('.md', '.html')
                dest_file_path = os.path.join(dest_dir_path, html_filename)
                
                # Generate the HTML page
                generate_page(item_path, template_path, dest_file_path)
        else:
            # It's a directory, recurse into it
            nested_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, nested_dest_dir)


def main():
    # Copy static files to public directory
    static_dir = "static"
    public_dir = "public"
    
    print("Starting static file copy process...")
    copy_static(static_dir, public_dir)
    print("Static file copy completed!")
    
    # Generate all pages recursively
    print("\nGenerating pages...")
    generate_pages_recursive(
        "content", 
        "template.html", 
        "public"
    )
    print("Page generation completed!")
    
    # Create a demo TextNode
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(f"\nDemo TextNode: {node}")


if __name__ == "__main__":
    main()