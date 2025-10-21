from markdown import markdown_to_html_node, code_block_to_html_node

# Test case 1 exactly as in the test file
md1 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

result1 = markdown_to_html_node(md1)
print("Test 1 result:")
print(repr(result1.to_html()))
print("Test 1 expected:")  
print(repr("<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"))
print("Match:", result1.to_html() == "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
print()

# Test case 2 - just the code block part from mixed test
md2 = "```\ncode block content\n```"
result2 = code_block_to_html_node(md2)
print("Test 2 result:")
print(repr(result2.to_html()))
print("Test 2 expected:")
print(repr("<pre><code>code block content</code></pre>"))
print("Match:", result2.to_html() == "<pre><code>code block content</code></pre>")