import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("a", "Click me!", None, props)
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Just a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        props = {"class": "highlight"}
        node = HTMLNode("div", "Content", None, props)
        expected = ' class="highlight"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode("p", "Test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        props = {"href": "https://www.boot.dev"}
        children = [HTMLNode("span", "child")]
        node = HTMLNode("a", "Boot.dev", children, props)
        expected = "HTMLNode(a, Boot.dev, [HTMLNode(span, child, None, None)], {'href': 'https://www.boot.dev'})"
        self.assertEqual(repr(node), expected)

    def test_values_none_by_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        props = {"href": "https://www.google.com"}
        node = LeafNode("a", "Click me!", props)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        props = {"href": "https://www.boot.dev", "target": "_blank", "class": "link"}
        node = LeafNode("a", "Boot.dev", props)
        expected = '<a href="https://www.boot.dev" target="_blank" class="link">Boot.dev</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_different_tags(self):
        # Test various HTML tags
        bold_node = LeafNode("b", "Bold text")
        self.assertEqual(bold_node.to_html(), "<b>Bold text</b>")
        
        code_node = LeafNode("code", "print('hello')")
        self.assertEqual(code_node.to_html(), "<code>print('hello')</code>")
        
        span_node = LeafNode("span", "Span content")
        self.assertEqual(span_node.to_html(), "<span>Span content</span>")

    def test_leaf_no_children(self):
        # Verify that LeafNode doesn't allow children (children should be None)
        node = LeafNode("p", "Text")
        self.assertIsNone(node.children)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode(None, "Normal text")
        child3 = LeafNode("i", "italic text")
        child4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child1, child2, child3, child4])
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        props = {"class": "container", "id": "main"}
        parent_node = ParentNode("div", [child_node], props)
        expected = '<div class="container" id="main"><span>child</span></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_nested_parent_nodes(self):
        # Create deeply nested structure
        innermost = LeafNode("em", "emphasized")
        middle = ParentNode("strong", [innermost])
        outer = ParentNode("p", [middle])
        expected = "<p><strong><em>emphasized</em></strong></p>"
        self.assertEqual(outer.to_html(), expected)

    def test_to_html_mixed_children(self):
        # Mix of LeafNodes and ParentNodes as children
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode(None, " and ")
        nested_leaf = LeafNode("em", "emphasized")
        parent_child = ParentNode("span", [nested_leaf])
        leaf3 = LeafNode(None, " text")
        
        parent_node = ParentNode("p", [leaf1, leaf2, parent_child, leaf3])
        expected = "<p><b>Bold</b> and <span><em>emphasized</em></span> text</p>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_no_tag_raises_error(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_to_html_no_children_raises_error(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have children")

    def test_to_html_empty_children_list(self):
        # Empty list should work (no children to render)
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_no_value(self):
        # Verify that ParentNode doesn't have a value (should be None)
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertIsNone(parent_node.value)


if __name__ == "__main__":
    unittest.main()