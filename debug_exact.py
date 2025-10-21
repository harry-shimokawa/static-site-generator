from markdown import markdown_to_blocks

# Let me reconstruct the exact markdown from the first test
md1_exact = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

print("Exact reconstruction:")
print("Original:", repr(md1_exact))
blocks1 = markdown_to_blocks(md1_exact)
print("Block:", repr(blocks1[0]))
extracted = blocks1[0][3:-3]
print("Extracted content:", repr(extracted))

# Let me try to see what would happen if there were double newlines
md1_double = '```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n\n```'
print("\nWith double newline:")
print("Test block:", repr(md1_double))
extracted_double = md1_double[3:-3]
print("Extracted:", repr(extracted_double))

# After stripping one leading and one trailing newline
if extracted_double.startswith('\n'):
    extracted_double = extracted_double[1:]
if extracted_double.endswith('\n'):
    extracted_double = extracted_double[:-1]
print("After stripping one each:", repr(extracted_double))