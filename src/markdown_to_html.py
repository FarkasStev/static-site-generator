from block_conversion import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from inline_conversion import text_node_to_html_node, text_to_textnodes
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def get_header_level(text):
    if text.startswith("#"):
        return text.count("#")
    return 0


def get_list_nodes(text):
    html_nodes = []
    for line in text.split("\n"):
        if line.startswith("-"):
            html_nodes.append(ParentNode("li", children=text_to_children(line[2:])))
        else:
            html_nodes.append(ParentNode("li", children=text_to_children(line[3:])))
    return html_nodes


def replace_greater_than(text):
    lines = []
    for line in text.split("\n"):
        line = line.replace(">", "")
        line = line.lstrip()
        lines.append(line)

    return "\n".join(lines)


def replace_newlines(text):
    return text.replace("\n", " ")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            nodes.append(
                ParentNode("p", children=text_to_children(replace_newlines(block)))
            )
        elif block_type == BlockType.CODE:
            nodes.append(
                ParentNode(
                    "pre",
                    children=[
                        text_node_to_html_node(TextNode(block[4:-3], TextType.CODE))
                    ],
                )
            )
        elif block_type == BlockType.ORDERED_LIST:
            nodes.append(ParentNode("ol", children=get_list_nodes(block)))
        elif block_type == BlockType.UNORDERED_LIST:
            nodes.append(ParentNode("ul", children=get_list_nodes(block)))
        elif block_type == BlockType.QUOTE:
            nodes.append(
                ParentNode(
                    "blockquote", children=text_to_children(replace_greater_than(block))
                )
            )
        elif block_type == BlockType.HEADING:
            nodes.append(
                ParentNode(
                    f"h{get_header_level(block)}",
                    children=text_to_children(block[get_header_level(block) + 1 :]),
                )
            )

    outer_div = ParentNode("div", children=nodes)

    return outer_div
