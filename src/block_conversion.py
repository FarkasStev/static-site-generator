from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped_block = block.strip()
        if len(stripped_block) > 0:
            result.append(stripped_block)

    return result


def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    curr_num = 0
    for line in lines:
        if block[0] == ">" and line[0] != ">":
            return BlockType.PARAGRAPH
        elif block[0:2] == "- " and line[0:2] != "- ":
            return BlockType.PARAGRAPH
        elif (
            block[0].isdigit()
            and line[0].isdigit()
            and line[1:3] == ". "
            and int(line[0]) == curr_num + 1
        ):
            curr_num += 1
        elif block[0].isdigit() and (
            line[1:3] != ". " or not line[0].isdigit() or int(line[0]) != curr_num + 1
        ):
            return BlockType.PARAGRAPH

    if block[0] == ">":
        return BlockType.QUOTE
    elif block[0:2] == "- ":
        return BlockType.UNORDERED_LIST
    elif block[0:3] == "1. ":
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
