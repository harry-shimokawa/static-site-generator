from markdown import markdown_to_blocks

# Test the full mixed blocks markdown to see the code block structure  
md_mixed = """# Main Heading

This is a paragraph with **bold** text.

## Subheading

> This is a quote

- List item 1
- List item 2

```
code block content
```

Another paragraph."""

print("Mixed blocks test:")
blocks = markdown_to_blocks(md_mixed)
for i, block in enumerate(blocks):
    print(f"Block {i}: {repr(block)}")
    
# Find the code block specifically
for i, block in enumerate(blocks):
    if block.startswith('```'):
        print(f"\nCode block (Block {i}):")
        print(f"Full block: {repr(block)}")
        extracted = block[3:-3]
        print(f"Extracted: {repr(extracted)}")
        
        # Apply current logic
        if extracted.startswith('\n'):
            processed = extracted[1:]
        else:
            processed = extracted
        print(f"After processing: {repr(processed)}")
        break