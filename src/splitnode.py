from textnode import TextType, TextNode

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
                    value = value.strip()
                    text_nodes = TextNode(value, node_type)
                    new_nodes.append(text_nodes)
                elif index % 2 != 0 and value != "":
                    node_type = text_type
                    value = value.strip()
                    text_nodes2 = TextNode(value, node_type)
                    new_nodes.append(text_nodes2)
    return new_nodes
                    