"""
HTMLNode module for representing HTML elements in a tree structure.

This module provides classes for creating and rendering HTML elements,
supporting both leaf nodes (no children) and parent nodes (with children).
Used as the target format for markdown-to-HTML conversion.
"""


class HTMLNode:
    """Base class for HTML nodes in a tree structure.
    
    Represents an HTML element with optional tag, value, children, and properties.
    This is an abstract base class - use LeafNode or ParentNode for concrete implementations.
    
    Attributes:
        tag (str, optional): The HTML tag name (e.g., 'p', 'div', 'a')
        value (str, optional): Text content for leaf nodes
        children (list, optional): Child HTMLNode objects for parent nodes  
        props (dict, optional): HTML attributes as key-value pairs
    """
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        """Initialize an HTMLNode.
        
        Args:
            tag (str, optional): HTML tag name. Defaults to None.
            value (str, optional): Text content. Defaults to None.
            children (list, optional): List of child nodes. Defaults to None.
            props (dict, optional): HTML attributes. Defaults to None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Convert the node to HTML string representation.
        
        This method should be implemented by subclasses.
        
        Raises:
            NotImplementedError: This is an abstract method
        """
        raise NotImplementedError

    def props_to_html(self):
        """Convert the node's properties to HTML attribute string.
        
        Converts the props dictionary to a string of HTML attributes
        in the format ' key="value" key2="value2"'.
        
        Returns:
            str: HTML attributes string, or empty string if no props
        """
        if self.props is None:
            return ""
        
        html_attrs = ""
        for key, value in self.props.items():
            html_attrs += f' {key}="{value}"'
        
        return html_attrs

    def __repr__(self):
        """Return string representation of HTMLNode.
        
        Returns:
            str: A string representation showing all node attributes
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """HTML node with no children (leaf node in the tree).
    
    Represents HTML elements that contain only text content and no child elements.
    Examples include <p>, <b>, <i>, <code>, <a>, etc.
    """
    
    def __init__(self, tag, value, props=None):
        """Initialize a LeafNode.
        
        Args:
            tag (str): HTML tag name, or None for raw text
            value (str): Text content of the node
            props (dict, optional): HTML attributes. Defaults to None.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """Convert the leaf node to HTML string.
        
        Returns the HTML representation of the node. If tag is None,
        returns just the value. Otherwise wraps value in the specified tag.
        
        Returns:
            str: HTML string representation
            
        Raises:
            ValueError: If value is None (all leaf nodes must have content)
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """HTML node with child nodes (parent node in the tree).
    
    Represents HTML elements that contain other HTML elements as children.
    Examples include <div>, <p>, <ul>, <ol>, etc. that wrap other content.
    """
    
    def __init__(self, tag, children, props=None):
        """Initialize a ParentNode.
        
        Args:
            tag (str): HTML tag name (required for parent nodes)
            children (list): List of child HTMLNode objects
            props (dict, optional): HTML attributes. Defaults to None.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """Convert the parent node and all children to HTML string.
        
        Recursively renders all child nodes and wraps them in this node's tag.
        
        Returns:
            str: HTML string representation with all children rendered
            
        Raises:
            ValueError: If tag is None or children is None
        """
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if self.children is None:
            raise ValueError("ParentNode must have children")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"