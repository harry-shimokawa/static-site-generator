import unittest
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from markdown import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_paragraphs(self):
        """Test the provided paragraph example"""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        """Test the provided codeblock example"""
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_heading(self):
        """Test heading conversion"""
        md = "# This is a **bold** heading"
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a <b>bold</b> heading</h1></div>"
        )
    
    def test_multiple_headings(self):
        """Test multiple heading levels"""
        md = """# Heading 1

## Heading 2 with *italic*

### Heading 3"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <i>italic</i></h2><h3>Heading 3</h3></div>"
        )
    
    def test_quote_block(self):
        """Test quote block conversion"""
        md = """> This is a quote
> with **bold** text
> on multiple lines"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith <b>bold</b> text\non multiple lines</blockquote></div>"
        )
    
    def test_unordered_list(self):
        """Test unordered list conversion"""
        md = """- First item with **bold**
- Second item with `code`
- Third item"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <code>code</code></li><li>Third item</li></ul></div>"
        )
    
    def test_ordered_list(self):
        """Test ordered list conversion"""
        md = """1. First item with *italic*
2. Second item
3. Third item with `code`"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <i>italic</i></li><li>Second item</li><li>Third item with <code>code</code></li></ol></div>"
        )
    
    def test_mixed_blocks(self):
        """Test document with multiple block types"""
        md = """# Main Heading

This is a paragraph with **bold** text.

## Subheading

> This is a quote

- List item 1
- List item 2

```
code block content
```

Another paragraph."""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Heading</h1>"
            "<p>This is a paragraph with <b>bold</b> text.</p>"
            "<h2>Subheading</h2>"
            "<blockquote>This is a quote</blockquote>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            "<pre><code>code block content</code></pre>"
            "<p>Another paragraph.</p>"
            "</div>"
        )
        self.assertEqual(html, expected)
    
    def test_empty_markdown(self):
        """Test empty markdown"""
        md = ""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
    
    def test_single_paragraph(self):
        """Test single paragraph"""
        md = "Just a simple paragraph."
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>Just a simple paragraph.</p></div>")


if __name__ == "__main__":
    unittest.main()