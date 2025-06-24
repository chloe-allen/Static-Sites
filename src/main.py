from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from convert import text_to_html_node
from splitnode import text_to_textnodes

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "url")
    print(node)

main()


def text_to_children(text):
    children_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_to_html_node(node)
        children_nodes.append(html_node)
    return children_nodes
    


def markdown_to_blocks(markdown):
    blocks = []
    import re
    split_text = re.split(r'\n\s*\n', markdown)
    for each_text in split_text:
        strip_text = each_text.strip()
        if strip_text != "":
            blocks.append(strip_text)
    return blocks

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_list = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_node = ParentNode(tag="p", children=text_to_children(block))
            html_node_list.append(html_node)
        
        
        elif block_type == BlockType.HEADING:
            count = 0
            index = 0
            while index < len(block) and block[index] == "#":
                count += 1
                index += 1
            
            if count == 1:
                html_node = ParentNode(tag="h1", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
            elif count == 2:
                html_node = ParentNode(tag="h2", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
            elif count == 3:
                html_node = ParentNode(tag="h3", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
            elif count == 4:
                html_node = ParentNode(tag="h4", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
            elif count == 5:
                html_node = ParentNode(tag="h5", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
            elif count == 6:
                html_node = ParentNode(tag="h6", children=text_to_children(block[index+1:]))
                html_node_list.append(html_node)
        
        elif block_type == BlockType.QUOTE:
            clean_text = []
            lines = block.split("\n")
            for line in lines:
                strip_text = line.strip("> ")
                clean_text.append(strip_text)
            joined_text = "\n".join(clean_text)
            html_node = ParentNode(tag="blockquote", children=text_to_children(joined_text))
            html_node_list.append(html_node)
        
        elif block_type == BlockType.UNORDERED_LIST:
            list_text = []
            split_block = block.split("\n")
            for line in split_block:
                clean_line = line[2:]
                html_node = ParentNode(tag="li", children=text_to_children(clean_line))
                list_text.append(html_node)
            html_node = ParentNode(tag="ul", children=list_text)
            html_node_list.append(html_node)

        elif block_type == BlockType.ORDERED_LIST:
            list_text = []
            split_block = block.split("\n")
            for line in split_block:
                index_line = line.find(".")
                clean_line = line[index_line + 2:]
                html_node_li = ParentNode(tag="li", children=text_to_children(clean_line))
                list_text.append(html_node_li)
            html_node_ol = ParentNode(tag="ol", children=list_text)
            html_node_list.append(html_node_ol)

        elif block_type == BlockType.CODE:
            code_node_list = []
            lines = block.split("\n")
            code_lines = lines[1:-1]
            min_indent = float('inf')
            for line in code_lines:
                if line.strip():
                    indent = len(line) - len(line.lstrip())
                    min_indent = min(min_indent, indent)
            if min_indent != float('inf'):
                dedented_lines = []
                for line in code_lines:
                    if line.strip():
                        dedented_lines.append(line[min_indent:])
                    else:
                        dedented_lines.append(line)
                code_content = "\n".join(dedented_lines)
            else:
                code_content = "\n".join(code_lines)
            
            if code_content and not code_content.endswith('\n'):
                code_content += '\n'

            text_node = TextNode(text=code_content, text_type=TextType.CODE)
            code_tag_node = text_to_html_node(text_node)
            code_node_list.append(code_tag_node)
            html_node = ParentNode(tag="pre", children=code_node_list)
            html_node_list.append(html_node)

    html_parent_node = ParentNode(tag="div", children=html_node_list)
        
    return html_parent_node