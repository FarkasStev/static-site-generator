def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        stripped_block = block.strip()
        if len(stripped_block) > 0:
            result.append(stripped_block)

    return result
