import unittest

from conversion import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        self.assertEqual(html_node.to_html(), "<i>This is a italic node</i>")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(html_node.to_html(), "<code>This is a code node</code>")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(
            html_node.to_html(), '<a href="google.com">This is a link node</a>'
        )

    def test_image_to_html(self):
        node = TextNode("This is a image node", TextType.IMAGE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.to_html(),
            '<img src="google.com" alt="This is a image node"></img>',
        )

    def test_no_delimeter(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        expected = [node, node2]
        self.assertEqual(expected, result)

    def test_bold_node_input(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        expected = [node, node2]
        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i], result[i])

    def test_bold_delimiter(self):
        node = TextNode("This is a *bold* node", TextType.TEXT)
        node2 = TextNode("*This* is a bold node", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        result_node = TextNode("This is a ", TextType.TEXT)
        result_node1 = TextNode("bold", TextType.BOLD)
        result_node2 = TextNode(" node", TextType.TEXT)
        result_node3 = TextNode("This", TextType.BOLD)
        result_node4 = TextNode(" is a bold node", TextType.TEXT)
        expected = [result_node, result_node1, result_node2, result_node3, result_node4]

        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i], result[i])

    def test_italic_delimiter(self):
        node = TextNode("This is _a_ italic node", TextType.TEXT)
        node2 = TextNode("This *is* a italic _node_", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        result_node = TextNode("This is ", TextType.TEXT)
        result_node1 = TextNode("a", TextType.ITALIC)
        result_node2 = TextNode(" italic node", TextType.TEXT)
        result_node3 = TextNode("This *is* a italic ", TextType.TEXT)
        result_node4 = TextNode("node", TextType.ITALIC)
        expected = [result_node, result_node1, result_node2, result_node3, result_node4]

        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i], result[i])

    def test_code_delimeter(self):
        node = TextNode("This is a `code` node", TextType.TEXT)
        node2 = TextNode("`This is a code node`", TextType.TEXT)
        result = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        result_node = TextNode("This is a ", TextType.TEXT)
        result_node1 = TextNode("code", TextType.CODE)
        result_node2 = TextNode(" node", TextType.TEXT)
        result_node3 = TextNode("This is a code node", TextType.CODE)
        expected = [result_node, result_node1, result_node2, result_node3]

        self.assertEqual(len(expected), len(result))
        for i in range(len(expected)):
            self.assertEqual(expected[i], result[i])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_with_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link1](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("link1", "https://i.imgur.com/zjjcJKZ.png"),
                ("link2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_leading_with_trailing(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and trailing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" and trailing", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_one_image_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_two_images_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/2zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/2zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_input(self):
        new_nodes = split_nodes_image([])
        self.assertListEqual(
            [],
            new_nodes,
        )
        new_nodes = split_nodes_image(None)
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_leading_with_trailing(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and trailing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link",
                    TextType.LINK,
                    "https://i.imgur.com/3elNhQu.png",
                ),
                TextNode(" and trailing", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_one_link_no_text(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_two_link_no_text(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)[link](https://i.imgur.com/2zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link", TextType.LINK, "https://i.imgur.com/2zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_empty_input(self):
        new_nodes = split_nodes_link([])
        self.assertListEqual(
            [],
            new_nodes,
        )
        new_nodes = split_nodes_link(None)
        self.assertListEqual(
            [],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
