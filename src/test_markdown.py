import unittest

from textnode import TextNode, TextType
from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        # Test the example from the assignment
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic phrase_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters_same_text(self):
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" blocks", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at the beginning", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("Text ending with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text ending with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("Just plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [node]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node_unchanged(self):
        # Non-TEXT nodes should pass through unchanged
        nodes = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Text with `code`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("Text with unmatched `delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertIn("unmatched delimiter", str(context.exception))

    def test_empty_delimiter_content(self):
        node = TextNode("Text with `` empty delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode(" empty delimiters", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_only_delimited_content(self):
        node = TextNode("`just code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("just code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_nodes_input(self):
        nodes = [
            TextNode("First `code` block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code` block", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(matches, expected)

    def test_extract_no_images(self):
        text = "This is text with no images, just [a link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_images_with_empty_alt(self):
        text = "Image with empty alt: ![](https://example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("", "https://example.com/image.jpg")])

    def test_extract_images_complex_alt_text(self):
        text = "![Alt text with spaces and symbols!@#](https://example.com/complex.png)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("Alt text with spaces and symbols!@#", "https://example.com/complex.png")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertEqual(matches, expected)

    def test_extract_single_link(self):
        text = "Check out [this link](https://example.com) for more info"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("this link", "https://example.com")])

    def test_extract_no_links(self):
        text = "This is just plain text with no links"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_extract_links_ignores_images(self):
        text = "This has ![image](https://example.com/img.jpg) and [link](https://example.com)"
        matches = extract_markdown_links(text)
        # Should only get the link, not the image
        self.assertEqual(matches, [("link", "https://example.com")])

    def test_extract_links_with_empty_text(self):
        text = "Empty link text: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("", "https://example.com")])

    def test_extract_links_complex_anchor_text(self):
        text = "[Complex anchor text with spaces and symbols!@#](https://example.com/complex)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("Complex anchor text with spaces and symbols!@#", "https://example.com/complex")])

    def test_mixed_images_and_links(self):
        text = "Here's an ![image](https://img.com/pic.jpg) and a [link](https://link.com) and another ![pic](https://img.com/pic2.jpg)"
        
        # Test that links function only gets links
        link_matches = extract_markdown_links(text)
        self.assertEqual(link_matches, [("link", "https://link.com")])
        
        # Test that images function only gets images
        image_matches = extract_markdown_images(text)
        expected_images = [
            ("image", "https://img.com/pic.jpg"),
            ("pic", "https://img.com/pic2.jpg")
        ]
        self.assertEqual(image_matches, expected_images)


if __name__ == "__main__":
    unittest.main()