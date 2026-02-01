from re import split
from textnode import TextNode, TextType



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) > 1 and len(split_node) % 3 > 0:
                raise Exception("Invalid Markdown")
            affected = False
            for new_node in split_node:
                if len(new_node) > 0:
                    if not affected:
                        new_nodes.append(TextNode(new_node, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(new_node, text_type))
                affected = not affected
    return new_nodes




    