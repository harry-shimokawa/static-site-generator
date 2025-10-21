"""
TextNode module for representing and converting markdown text elements.

This module provides classes and functions for handling different types of text
nodes in a markdown parser, including plain text, bold, italic, code, links,
and images. It also provides conversion functionality to HTML nodes.
"""
from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    """Enumeration of supported text node types in markdown.
    
    Attributes:
        TEXT: Plain text content
        BOLD: Bold text (**text**)
        ITALIC: Italic text (*text* or _text_)
        CODE: Inline code (`text`)
        LINK: Hyperlink ([text](url))
        IMAGE: Image (![alt](url))
    """
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Represents a node of text with a specific type and optional URL.
    
    A TextNode is an intermediate representation used in markdown parsing
    to represent different types of text content before conversion to HTML.
    
    Attributes:
        text (str): The text content of the node
        text_type (TextType): The type of text (plain, bold, italic, etc.)
        url (str, optional): URL for links and images, None for other types
    """
    
    def __init__(self, text, text_type, url=None):
        """Initialize a TextNode.
        
        Args:
            text (str): The text content
            text_type (TextType): The type of the text node
            url (str, optional): URL for links/images. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        """Check equality with another TextNode.
        
        Args:
            other (TextNode): Another TextNode to compare with
            
        Returns:
            bool: True if all attributes are equal, False otherwise
        """
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
    
    def __repr__(self):
        """Return string representation of the TextNode.
        
        Returns:
            str: A string representation showing text, type, and URL
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """Convert a TextNode to an appropriate HTMLNode.
    
    This function converts TextNode objects into LeafNode HTML elements
    based on their text type. Each text type maps to a specific HTML tag:
    - TEXT: Raw text content (no tag)
    - BOLD: <b> tag
    - ITALIC: <i> tag  
    - CODE: <code> tag
    - LINK: <a> tag with href attribute
    - IMAGE: <img> tag with src and alt attributes
    
    Args:
        text_node (TextNode): The TextNode to convert
        
    Returns:
        LeafNode: An HTML leaf node representing the text content
        
    Raises:
        ValueError: If the text_node has an unsupported text_type
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
