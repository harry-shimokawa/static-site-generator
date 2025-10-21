import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Split the text on the delimiter
        parts = old_node.text.split(delimiter)
        
        # If there's an odd number of parts, we have unmatched delimiters
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}'")
        
        # Process the parts
        for i, part in enumerate(parts):
            if not part:  # Skip empty parts
                continue
                
            if i % 2 == 0:
                # Even indices are normal text
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Odd indices are the delimited text (e.g., bold, italic, code)
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes


def extract_markdown_images(text):
    """
    Extract markdown images from text.
    Returns a list of tuples: (alt_text, url)
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extract markdown links from text (excluding images).
    Returns a list of tuples: (anchor_text, url)
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    """
    Split TextNodes containing markdown images into separate nodes.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(old_node.text)
        
        # If no images found, add the original node
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Split the text around each image
        current_text = old_node.text
        
        for image_alt, image_url in images:
            # Split on the full image markdown syntax
            image_markdown = f"![{image_alt}]({image_url})"
            sections = current_text.split(image_markdown, 1)
            
            if len(sections) != 2:
                continue  # This shouldn't happen if extraction worked correctly
            
            # Add the text before the image (if not empty)
            before_text = sections[0]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            
            # Continue with the text after the image
            current_text = sections[1]
        
        # Add any remaining text after the last image (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes containing markdown links into separate nodes.
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # If the node is not a TEXT type, add it as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(old_node.text)
        
        # If no links found, add the original node
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Split the text around each link
        current_text = old_node.text
        
        for link_text, link_url in links:
            # Split on the full link markdown syntax
            link_markdown = f"[{link_text}]({link_url})"
            sections = current_text.split(link_markdown, 1)
            
            if len(sections) != 2:
                continue  # This shouldn't happen if extraction worked correctly
            
            # Add the text before the link (if not empty)
            before_text = sections[0]
            if before_text:
                new_nodes.append(TextNode(before_text, TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            
            # Continue with the text after the link
            current_text = sections[1]
        
        # Add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def text_to_textnodes(text):
    """
    Convert raw markdown text to a list of TextNode objects.
    
    This function applies all splitting operations in the correct order:
    1. Bold (**text**)
    2. Italic (_text_)  
    3. Code (`text`)
    4. Images (![alt](url))
    5. Links ([text](url))
    """
    # Start with a single TEXT node containing all the text
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Apply all delimiter splitting first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Then split images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes


def markdown_to_blocks(markdown):
    """
    Split a raw markdown string into block-level elements.
    
    Blocks are separated by blank lines (double newlines).
    Leading and trailing whitespace is stripped from each block.
    Empty blocks are removed.
    """
    # Split on double newlines to separate blocks
    blocks = markdown.split("\n\n")
    
    # Strip whitespace and filter out empty blocks
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:  # Only add non-empty blocks
            cleaned_blocks.append(stripped_block)
    
    return cleaned_blocks