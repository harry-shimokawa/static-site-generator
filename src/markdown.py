import re
from enum import Enum
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
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


def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Returns the BlockType enum value for the given block.
    Assumes leading and trailing whitespace has already been stripped.
    """
    # Check for heading (1-6 # characters followed by space)
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with 3 backticks)
    if block.startswith('```') and block.endswith('```') and len(block) >= 6:
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check for ordered list (lines start with number. followed by space, incrementing from 1)
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_number = i + 1
        if not re.match(rf'^{expected_number}\. ', line):
            is_ordered_list = False
            break
    
    if is_ordered_list and len(lines) > 0:
        return BlockType.ORDERED_LIST
    
    # Default to paragraph if no other patterns match
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Convert a text string with inline markdown to a list of HTMLNodes.
    
    Uses existing text_to_textnodes and text_node_to_html_node functions.
    """
    from textnode import text_node_to_html_node
    
    # Convert text to TextNodes using existing function
    text_nodes = text_to_textnodes(text)
    
    # Convert TextNodes to HTMLNodes
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    
    return children


def markdown_to_html_node(markdown):
    """
    Convert a full markdown document into a single parent HTMLNode.
    
    Returns a div HTMLNode containing child nodes for each block.
    """
    from htmlnode import ParentNode
    
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Process each block into HTMLNode
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_block_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)
        else:
            # Fallback to paragraph
            block_node = paragraph_to_html_node(block)
        
        block_nodes.append(block_node)
    
    # Create parent div node with all block nodes as children
    return ParentNode("div", block_nodes)


def paragraph_to_html_node(block):
    """Convert a paragraph block to an HTML p node."""
    from htmlnode import ParentNode
    # Join multiple lines in paragraph with spaces
    paragraph_text = " ".join(line.strip() for line in block.split('\n'))
    children = text_to_children(paragraph_text)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Convert a heading block to an HTML h1-h6 node."""
    from htmlnode import ParentNode
    
    # Count the number of # characters
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # Extract the heading text (skip the # characters and space)
    heading_text = block[level:].strip()
    
    # Create the appropriate heading tag
    tag = f"h{level}"
    children = text_to_children(heading_text)
    return ParentNode(tag, children)


def code_block_to_html_node(block):
    """Convert a code block to HTML pre/code nodes."""
    from htmlnode import ParentNode
    from textnode import text_node_to_html_node
    
    # Remove the opening and closing backticks
    code_content = block[3:-3]  # Remove ``` from start and end
    
    # Strip leading newlines only, preserve trailing structure exactly as written
    # This matches the expected behavior in the tests
    if code_content.startswith('\n'):
        code_content = code_content[1:]
    
    # For code blocks, we don't parse inline markdown
    # Create a simple text node and convert it
    text_node = TextNode(code_content, TextType.TEXT)
    code_node = text_node_to_html_node(text_node)
    
    # Wrap in code tag, then pre tag
    code_parent = ParentNode("code", [code_node])
    return ParentNode("pre", [code_parent])


def quote_to_html_node(block):
    """Convert a quote block to HTML blockquote node."""
    from htmlnode import ParentNode
    
    # Remove the > characters from each line
    lines = block.split('\n')
    quote_lines = []
    for line in lines:
        # Remove the > and any space after it
        if line.startswith('> '):
            quote_lines.append(line[2:])
        elif line.startswith('>'):
            quote_lines.append(line[1:])
        else:
            quote_lines.append(line)
    
    # Join lines back together
    quote_text = '\n'.join(quote_lines)
    
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    """Convert an unordered list block to HTML ul/li nodes."""
    from htmlnode import ParentNode
    
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Remove the '- ' from the beginning
        item_text = line[2:]  # Remove '- '
        item_children = text_to_children(item_text)
        list_item = ParentNode("li", item_children)
        list_items.append(list_item)
    
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block):
    """Convert an ordered list block to HTML ol/li nodes."""
    from htmlnode import ParentNode
    
    lines = block.split('\n')
    list_items = []
    
    for line in lines:
        # Find the '. ' pattern and remove everything up to it
        dot_index = line.find('. ')
        if dot_index != -1:
            item_text = line[dot_index + 2:]  # Skip past '. '
            item_children = text_to_children(item_text)
            list_item = ParentNode("li", item_children)
            list_items.append(list_item)
    
    return ParentNode("ol", list_items)