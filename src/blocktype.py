from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):
    lines = markdown.splitlines()
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines) :
        return BlockType.UNORDERED_LIST
    
    for number, line in enumerate(lines, start=1):
        if not line.startswith(f"{number}. "):
            break 
    else:
        return BlockType.ORDERED_LIST

    count = 0
    i = 0
    while i < len(markdown) and markdown[i] == "#":  
        count += 1
        i += 1
    if count in range(1, 7) and i < len(markdown) and markdown[i] == " ":
        return BlockType.HEADING

    
    return BlockType.PARAGRAPH 

