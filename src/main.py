from textnode import TextNode, TextType

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "url")
    print(node)

main()
