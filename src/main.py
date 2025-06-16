from textnode import TextNode, TextType

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "url")
    print(node)

main()

def markdown_to_blocks(markdown):
    blocks = []
    split_text = markdown.split("\n\n")
    for each_text in split_text:
        strip_text = each_text.strip()
        if strip_text != "":
            blocks.append(strip_text)
    return blocks