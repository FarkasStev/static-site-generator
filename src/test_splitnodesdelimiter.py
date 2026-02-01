import unittest

from textnode import TextNode, TextType
from splitnodesdelimiter import split_nodes_delimiter


class TestSplitnodesdelimeter(unittest.TestCase):
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

    def test_bold(self):
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

    def test_italic(self):
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

    def test_code(self):
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
if __name__ == "__main__":
    unittest.main()