import unittest

from block_conversion import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
)


class TestBlockConversion(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items





    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_input(self):
        md = """

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("#This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##This is a heading"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(
            block_to_block_type("```\nThis is a code block```"), BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```\nThis is not a code block``"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("``\nThis is not a code block```"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type(
                "This is a paragraph\nThis is the same paragraph on a new line"
            ),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- This is a list\n- with items"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("- This is a list\n-with items"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. This is a list\n3. with items"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. This is a list\n2.with items"), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("1. This is a list\n2. with items"),
            BlockType.ORDERED_LIST,
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# This is a title"), "This is a title")
        self.assertEqual(
            extract_title("# This is a title\nThis is a paragraph"), "This is a title"
        )
        try:
            extract_title("## This is a title\nThis is a paragraph")
        except Exception as e:
            self.assertEqual(str(e), "No title found")
        try:
            extract_title("This is a paragraph")
        except Exception as e:
            self.assertEqual(str(e), "No title found")
