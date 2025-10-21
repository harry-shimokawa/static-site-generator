# Let me examine the exact content of both test cases more precisely

# Test 1: codeblock test
md1 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

print("Codeblock test analysis:")
print("Full markdown:", repr(md1))

from markdown import markdown_to_blocks
blocks1 = markdown_to_blocks(md1)
code_block = blocks1[0]
print("Code block:", repr(code_block))
extracted = code_block[3:-3]
print("Extracted:", repr(extracted))
print("Length:", len(extracted))

# Count newlines
leading_newlines = 0
for char in extracted:
    if char == '\n':
        leading_newlines += 1
    else:
        break

trailing_newlines = 0
for char in reversed(extracted):
    if char == '\n':
        trailing_newlines += 1
    else:
        break

print(f"Leading newlines: {leading_newlines}")
print(f"Trailing newlines: {trailing_newlines}")

print("\n" + "="*50 + "\n")

# Test 2: mixed blocks test (just the code part)
md2_full = """# Main Heading

This is a paragraph with **bold** text.

## Subheading

> This is a quote

- List item 1
- List item 2

```
code block content
```

Another paragraph."""

blocks2 = markdown_to_blocks(md2_full)
code_block2 = None
for block in blocks2:
    if block.startswith('```'):
        code_block2 = block
        break

print("Mixed blocks test analysis:")
print("Code block:", repr(code_block2))
extracted2 = code_block2[3:-3]
print("Extracted:", repr(extracted2))
print("Length:", len(extracted2))

# Count newlines
leading_newlines2 = 0
for char in extracted2:
    if char == '\n':
        leading_newlines2 += 1
    else:
        break

trailing_newlines2 = 0
for char in reversed(extracted2):
    if char == '\n':
        trailing_newlines2 += 1
    else:
        break

print(f"Leading newlines: {leading_newlines2}")
print(f"Trailing newlines: {trailing_newlines2}")