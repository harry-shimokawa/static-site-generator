from markdown import heading_to_html_node

md = "## Heading 2 with *italic*"
print("Original:", repr(md))

result = heading_to_html_node(md)
print("Heading result:", result.to_html())