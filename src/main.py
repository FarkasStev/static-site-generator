from textnode import TextNode, TextType

def main():
    testNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(testNode)




main()