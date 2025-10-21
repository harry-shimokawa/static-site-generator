from markdown import text_to_children

text = "Heading 2 with *italic*"
print("Original:", repr(text))

children = text_to_children(text)
print("Children:")
for child in children:
    print(f"  {child.to_html()}")

# Let's also test the text_to_textnodes function
from markdown import text_to_textnodes
nodes = text_to_textnodes(text)
print("TextNodes:")
for node in nodes:
    print(f"  {node.text}, {node.text_type}")