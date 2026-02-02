import re

from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid text type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 > 0:
                raise Exception("Invalid Markdown")
            split_node = node.text.split(delimiter)
            affected = False
            for new_node in split_node:
                if len(new_node) > 0:
                    if not affected:
                        new_nodes.append(TextNode(new_node, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(new_node, text_type))
                affected = not affected
    return new_nodes


def extract_markdown_images(text):
    pattern = r"\!\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    nodes = []
    if old_nodes is None:
        return nodes
    for node in old_nodes:
        current_text = node.text
        images = extract_markdown_images(node.text)
        if len(images) > 0:
            for i in range(len(images)):
                image_alt = images[i][0]
                image_link = images[i][1]
                current_split = current_text.split(f"![{image_alt}]({image_link})", 1)
                preceding_text = current_split[0]
                current_text = current_split[1]
                if len(preceding_text) > 0:
                    nodes.append(TextNode(preceding_text, TextType.TEXT))
                nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if len(current_text) > 0:
                nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            nodes.append(node)

    return nodes


def split_nodes_link(old_nodes):
    nodes = []
    if old_nodes is None:
        return nodes
    for node in old_nodes:
        current_text = node.text
        links = extract_markdown_links(node.text)
        if len(links) > 0:
            for i in range(len(links)):
                link_text = links[i][0]
                link_target = links[i][1]
                current_split = current_text.split(f"[{link_text}]({link_target})", 1)
                preceding_text = current_split[0]
                current_text = current_split[1]
                if len(preceding_text) > 0:
                    nodes.append(TextNode(preceding_text, TextType.TEXT))
                nodes.append(TextNode(link_text, TextType.LINK, link_target))
            if len(current_text) > 0:
                nodes.append(TextNode(current_text, TextType.TEXT))
        else:
            nodes.append(node)
    return nodes


def text_to_textnodes(text):
    initial_node = [TextNode(text, TextType.TEXT)]
    bolded_nodes = split_nodes_delimiter(initial_node, "**", TextType.BOLD)
    italicized_nodes = split_nodes_delimiter(bolded_nodes, "_", TextType.ITALIC)
    coded_nodes = split_nodes_delimiter(italicized_nodes, "`", TextType.CODE)
    imaged_nodes = split_nodes_image(coded_nodes)
    linked_nodes = split_nodes_link(imaged_nodes)
    return linked_nodes
