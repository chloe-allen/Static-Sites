from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type.TEXT:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0 :
                raise ValueError ("delimiter is not found")
            for index, value in enumerate(split_nodes):
                if index % 2 == 0 and value != "":
                    node_type = TextType.TEXT
                    
                    text_nodes = TextNode(value, node_type)
                    new_nodes.append(text_nodes)
                elif index % 2 != 0 and value != "":
                    node_type = text_type
                    
                    text_nodes2 = TextNode(value, node_type)
                    new_nodes.append(text_nodes2)
    return new_nodes
                    

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if extract_markdown_images(node.text) == []:
            new_nodes.append(node)
        else:
            extract_node = extract_markdown_images(node.text)
            first_image = extract_node[0]
            text = first_image[0]
            url = first_image[1]
            nodes = node.text.split(f"![{text}]({url})", 1)  
            text_node = TextNode(text=nodes[0], text_type=TextType.TEXT)
            if nodes[0] != "":
                new_nodes.append(text_node)
            text_node2 = TextNode(text=text, text_type=TextType.IMAGE, url=url)
            new_nodes.append(text_node2)
            if nodes[1] != "":
                more_nodes = split_nodes_image([TextNode(nodes[1], TextType.TEXT)])
                new_nodes.extend(more_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if extract_markdown_links(node.text) == []:
            new_nodes.append(node)
        else:
            extract_node = extract_markdown_links(node.text)
            first_link = extract_node[0]
            text = first_link[0]
            url = first_link[1]
            nodes = node.text.split(f"[{text}]({url})", 1)
            text_node = TextNode(text=nodes[0], text_type=TextType.TEXT)
            if nodes[0] != "":
                new_nodes.append(text_node)
            text_node2 = TextNode(text=text, text_type=TextType.LINK, url=url)
            new_nodes.append(text_node2)
            if nodes[1] != "":
                more_nodes = split_nodes_link([TextNode(nodes[1], TextType.TEXT)])
                new_nodes.extend(more_nodes)
    return new_nodes

           
def text_to_textnodes(text):
    new_nodes= []
    if text != "":
        text_node = TextNode(text=text, text_type=TextType.TEXT)
        new_nodes.append(text_node)
        split_bold_delimiter = split_nodes_delimiter(old_nodes=new_nodes, delimiter="**", text_type=TextType.BOLD)
        new_nodes = split_bold_delimiter 
        split_italic_delimiter = split_nodes_delimiter(old_nodes=new_nodes, delimiter="_", text_type=TextType.ITALIC)
        new_nodes = split_italic_delimiter
        split_code_delimiter = split_nodes_delimiter(old_nodes=new_nodes, delimiter="`", text_type=TextType.CODE) 
        new_nodes = split_code_delimiter

        split_image = split_nodes_image(new_nodes)
        new_nodes = split_image     
        split_link = split_nodes_link(new_nodes)
        new_nodes = split_link
    return new_nodes       
                
                
                
                
        


                
                
          