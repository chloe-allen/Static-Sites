from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode, ParentNode, LeafNode
from convert import text_to_html_node
from splitnode import text_to_textnodes
import shutil
import os
from pathlib import Path

def main():
    
    recursive_copy('static', 'public')
    generate_pages_recursive("content", "template.html", "public")
    

def recursive_copy(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            recursive_copy(src_path, dst_path)


def generate_page(from_path, template_path, dest_path):
    print(f"generate_page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()
        
    markdown_html = markdown_to_html_node(markdown_content)
    html_content = markdown_html.to_html()
    markdown_title = extract_title(markdown_content)
    page = template_content.replace("{{ Title }}", markdown_title)
    page = page.replace("{{ Content }}", html_content)
    dir_name = os.path.dirname(dest_path)
    os.makedirs(dir_name, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    with open(template_path, "r") as f:
        template_content = f.read()
   
    contents = os.listdir(dir_path_content)
    for item_name in contents:
        isFile = os.path.isfile(os.path.join(dir_path_content, item_name))
        if isFile is True and item_name.endswith(".md"):
            with open(os.path.join(dir_path_content, item_name), "r") as f:
                markdown_content = f.read()
            markdown_html = markdown_to_html_node(markdown_content)
            html_content = markdown_html.to_html()
            page = template_content.replace("{{ Content }}", html_content)
            root_ext = os.path.splitext(os.path.join(dir_path_content, item_name))
            relative_path = os.path.relpath(root_ext[0], dir_path_content)
            dest_file_path = os.path.join(dest_dir_path, relative_path) + ".html"
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            with open(dest_file_path, "w") as f:
                f.write(page)
        elif os.path.isdir(os.path.join(dir_path_content, item_name)):
            generate_pages_recursive(os.path.join(dir_path_content, item_name), template_path, os.path.join(dest_dir_path, item_name))
            


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        find_header = line.startswith("# ")
        if find_header == True:
            header = line[2:]
            clean_header = header.strip()
            return clean_header
    else:
        raise ValueError("no header")
    


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


main()


