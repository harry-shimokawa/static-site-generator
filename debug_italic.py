from markdown import text_to_textnodes

# Test with underscore italic  
text1 = "Heading 2 with _italic_"
print("With underscore:", repr(text1))
nodes1 = text_to_textnodes(text1)
for node in nodes1:
    print(f"  {node.text}, {node.text_type}")

# Test with asterisk italic
text2 = "Heading 2 with *italic*"  
print("With asterisk:", repr(text2))
nodes2 = text_to_textnodes(text2)
for node in nodes2:
    print(f"  {node.text}, {node.text_type}")