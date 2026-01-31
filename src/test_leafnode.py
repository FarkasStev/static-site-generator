import unittest

from leafnode import LeafNode 

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_link(self):
        node = LeafNode("link", "Hello, world!")
        self.assertEqual(node.to_html(), "<link>Hello, world!</link>")

    def test_leaf_to_html_body(self):
        node = LeafNode("body", "Hello, world!")
        self.assertEqual(node.to_html(), "<body>Hello, world!</body>")