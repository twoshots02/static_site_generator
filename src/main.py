from textnode import *
from enum import Enum
from htmlnode import *
from inline import *


def main():
#    text_node = TextNode("This is a text node", TextType.BOLD.value, "https://www.boot.dev")
#    print(f"TextNode({text_node.text}, {text_node.text_type}, {text_node.url})")
#    print(text_node.text)
#    print(text_node.text_type)
#    print(text_node.url)
#    delimiter_node3 = TextNode("** **bold** **", TextType.NORMAL)
#    result3 = split_nodes_delimiter([delimiter_node3], "**", TextType.BOLD)
#    print(f"the results are: {result3}")
# Test just one specific case
# Test case 1
    #node = TextNode("This is a [link](https://boot.dev) with text", TextType.NORMAL)
    #result = split_nodes_link([node])
    #print("\nTest case 1 (should produce 4 nodes):")
    #print("Input:", node.text)
    #for n in result:
    #    print(f"Text: '{n.text}', Type: {n.text_type}, URL: {n.url}")

        # Test case 2
   # node = TextNode("[link one](url1) then [link two](url2)", TextType.NORMAL)
   # result = split_nodes_link([node])
   # print("\nTest case 2 (should produce 3 nodes):")
   # print("Input:", node.text)
   # for n in result:
   #     print(f"Text: '{n.text}', Type: {n.text_type}, URL: {n.url}")    

    node = TextNode("Start [first link](https://example.com) middle [second link](https://boot.dev) end", TextType.NORMAL)
    result = split_nodes_link([node])
    print("\nTest multiple links:")
    print("Input:", node.text)
    for n in result:
        print(f"Text: '{n.text}', Type: {n.text_type}, URL: {n.url}")
main()