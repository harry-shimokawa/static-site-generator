from markdown import code_block_to_html_node

md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
print("Original:", repr(md))
print("Extracted content:", repr(md[3:-3]))

result = code_block_to_html_node(md)
print("Code block result:", result.to_html())