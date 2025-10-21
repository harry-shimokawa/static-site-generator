import unittest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    
    def test_markdown_to_blocks_basic(self):
        """Test the provided example from the assignment"""
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_with_whitespace(self):
        """Test that leading and trailing whitespace is stripped"""
        markdown = """  # Heading with spaces  

  Paragraph with spaces  

  * List item with spaces  """
        
        expected = [
            "# Heading with spaces",
            "Paragraph with spaces",
            "* List item with spaces"
        ]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_empty_blocks(self):
        """Test that empty blocks are removed"""
        markdown = """# First heading



# Second heading



Paragraph after empty blocks"""
        
        expected = [
            "# First heading",
            "# Second heading",
            "Paragraph after empty blocks"
        ]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_single_block(self):
        """Test with a single block (no double newlines)"""
        markdown = "This is just one block with no separators."
        expected = ["This is just one block with no separators."]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_empty_string(self):
        """Test with an empty string"""
        markdown = ""
        expected = []
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_only_whitespace(self):
        """Test with only whitespace"""
        markdown = "   \n\n   \n\n   "
        expected = []
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_mixed_separators(self):
        """Test with various amounts of newlines"""
        markdown = """First block

Second block



Third block




Fourth block"""
        
        expected = [
            "First block",
            "Second block",
            "Third block",
            "Fourth block"
        ]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)
    
    def test_markdown_to_blocks_preserve_internal_newlines(self):
        """Test that single newlines within blocks are preserved"""
        markdown = """# Heading

This is a paragraph
with multiple lines
that should stay together

Another paragraph
also with multiple lines"""
        
        expected = [
            "# Heading",
            "This is a paragraph\nwith multiple lines\nthat should stay together",
            "Another paragraph\nalso with multiple lines"
        ]
        
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()