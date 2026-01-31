import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        testNode = HTMLNode("p", "paragraph text", props={"href": "https://www.google.com"})
        self.assertEqual(testNode.props_to_html(), " href=\"https://www.google.com\"")

    def test_props_to_html_multiple(self):
        testNode = HTMLNode("p", "paragraph text", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(testNode.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_props_to_html_none(self):
        testNode = HTMLNode("p", "paragraph text")
        self.assertEqual(testNode.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()