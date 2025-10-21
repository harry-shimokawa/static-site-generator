from markdown import markdown_to_blocks

# Test what blocks are created for both test cases

# Test case 1: From test_codeblock  
md1 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

print("Test case 1 markdown:")
print("Original:", repr(md1))
blocks1 = markdown_to_blocks(md1)
print("Blocks:", len(blocks1))
for i, block in enumerate(blocks1):
    print(f"Block {i}: {repr(block)}")
print()

# Test case 2: From test_mixed_blocks (just the code block part)
md2 = """```
code block content
```"""

print("Test case 2 markdown:")
print("Original:", repr(md2))
blocks2 = markdown_to_blocks(md2)
print("Blocks:", len(blocks2))
for i, block in enumerate(blocks2):
    print(f"Block {i}: {repr(block)}")