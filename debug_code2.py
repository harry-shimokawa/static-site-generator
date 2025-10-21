# Test both code block scenarios
from markdown import code_block_to_html_node

# Test case 1: From test_codeblock (has trailing newline)
md1 = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
print("Test case 1 (with trailing newline):")
print("Original:", repr(md1))
print("Extracted:", repr(md1[3:-3]))
result1 = code_block_to_html_node(md1)
print("Result:", result1.to_html())
print()

# Test case 2: From test_mixed_blocks (no trailing newline) 
md2 = "```\ncode block content\n```"
print("Test case 2 (without trailing newline):")
print("Original:", repr(md2))
print("Extracted:", repr(md2[3:-3]))
result2 = code_block_to_html_node(md2)
print("Result:", result2.to_html())