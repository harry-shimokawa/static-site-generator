import unittest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from markdown import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    
    def test_heading_blocks(self):
        """Test various heading levels"""
        # H1
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        # H2
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        # H3
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        # H4
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEADING)
        # H5
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEADING)
        # H6
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
    
    def test_invalid_headings(self):
        """Test that invalid headings are not detected as headings"""
        # Too many # characters
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)
        # No space after #
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        # # in middle of text
        self.assertEqual(block_to_block_type("This is # not a heading"), BlockType.PARAGRAPH)
    
    def test_code_blocks(self):
        """Test code block detection"""
        # Basic code block
        self.assertEqual(block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE)
        # Code block with language
        self.assertEqual(block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE)
        # Minimal code block
        self.assertEqual(block_to_block_type("``````"), BlockType.CODE)
    
    def test_invalid_code_blocks(self):
        """Test that invalid code blocks are not detected"""
        # Only opening backticks
        self.assertEqual(block_to_block_type("```\ncode without closing"), BlockType.PARAGRAPH)
        # Only closing backticks
        self.assertEqual(block_to_block_type("code without opening\n```"), BlockType.PARAGRAPH)
        # Too few backticks
        self.assertEqual(block_to_block_type("``code``"), BlockType.PARAGRAPH)
        # Backticks in middle
        self.assertEqual(block_to_block_type("some ``` code"), BlockType.PARAGRAPH)
    
    def test_quote_blocks(self):
        """Test quote block detection"""
        # Single line quote
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        # Multi-line quote
        multi_line_quote = ">This is line 1\n>This is line 2\n>This is line 3"
        self.assertEqual(block_to_block_type(multi_line_quote), BlockType.QUOTE)
        # Quote with spaces after >
        self.assertEqual(block_to_block_type("> Quote with space"), BlockType.QUOTE)
    
    def test_invalid_quotes(self):
        """Test that invalid quotes are not detected as quote blocks"""
        # Missing > on one line
        invalid_quote = ">This is quoted\nThis is not quoted\n>This is quoted again"
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)
        # > in middle of text
        self.assertEqual(block_to_block_type("This > is not a quote"), BlockType.PARAGRAPH)
    
    def test_unordered_list_blocks(self):
        """Test unordered list detection"""
        # Single item list
        self.assertEqual(block_to_block_type("- List item"), BlockType.UNORDERED_LIST)
        # Multi-item list
        multi_item_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(multi_item_list), BlockType.UNORDERED_LIST)
        # List with longer text
        long_list = "- This is a longer list item with more text\n- Another item"
        self.assertEqual(block_to_block_type(long_list), BlockType.UNORDERED_LIST)
    
    def test_invalid_unordered_lists(self):
        """Test that invalid unordered lists are not detected"""
        # Missing space after -
        self.assertEqual(block_to_block_type("-No space after dash"), BlockType.PARAGRAPH)
        # Missing - on one line
        invalid_list = "- Item 1\nNot a list item\n- Item 3"
        self.assertEqual(block_to_block_type(invalid_list), BlockType.PARAGRAPH)
        # - in middle of text
        self.assertEqual(block_to_block_type("This - is not a list"), BlockType.PARAGRAPH)
    
    def test_ordered_list_blocks(self):
        """Test ordered list detection"""
        # Single item list
        self.assertEqual(block_to_block_type("1. First item"), BlockType.ORDERED_LIST)
        # Multi-item list
        multi_item_ordered = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(multi_item_ordered), BlockType.ORDERED_LIST)
        # Longer list
        long_ordered = "1. Item one\n2. Item two\n3. Item three\n4. Item four\n5. Item five"
        self.assertEqual(block_to_block_type(long_ordered), BlockType.ORDERED_LIST)
    
    def test_invalid_ordered_lists(self):
        """Test that invalid ordered lists are not detected"""
        # Wrong starting number
        self.assertEqual(block_to_block_type("2. Starting at 2"), BlockType.PARAGRAPH)
        # Non-sequential numbers
        invalid_sequence = "1. First\n3. Third (skipped 2)\n4. Fourth"
        self.assertEqual(block_to_block_type(invalid_sequence), BlockType.PARAGRAPH)
        # Missing space after number and dot
        self.assertEqual(block_to_block_type("1.No space"), BlockType.PARAGRAPH)
        # Missing dot after number
        self.assertEqual(block_to_block_type("1 Missing dot"), BlockType.PARAGRAPH)
        # Numbers out of order
        wrong_order = "1. First\n2. Second\n1. Back to one"
        self.assertEqual(block_to_block_type(wrong_order), BlockType.PARAGRAPH)
    
    def test_paragraph_blocks(self):
        """Test that regular paragraphs are detected correctly"""
        # Simple paragraph
        self.assertEqual(block_to_block_type("This is a regular paragraph."), BlockType.PARAGRAPH)
        # Multi-line paragraph
        multi_line = "This is a paragraph\nwith multiple lines\nthat should be treated as one block."
        self.assertEqual(block_to_block_type(multi_line), BlockType.PARAGRAPH)
        # Paragraph with special characters
        special_chars = "This paragraph has special chars: @#$%^&*()"
        self.assertEqual(block_to_block_type(special_chars), BlockType.PARAGRAPH)
        # Empty string should be paragraph
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
    
    def test_edge_cases(self):
        """Test various edge cases"""
        # Mixed content - this IS a heading because it starts with # followed by space
        # (the function is designed to check block type based on the start pattern)
        mixed = "# Heading\nBut then regular text\nSo it's still a heading block"
        self.assertEqual(block_to_block_type(mixed), BlockType.HEADING)
        
        # Text that looks like markdown but isn't quite right
        almost_quote = "Almost > a quote but not quite"
        self.assertEqual(block_to_block_type(almost_quote), BlockType.PARAGRAPH)
        
        # Text with markdown-like characters
        markdown_chars = "This has * and ** and _ characters but is still a paragraph"
        self.assertEqual(block_to_block_type(markdown_chars), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()