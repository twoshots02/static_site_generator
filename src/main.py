from textnode import *
from enum import Enum
from htmlnode import *
from inline import *
from splitblocks import *


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

# Test ordered list
    #print(block_to_block_type("1. First\n2. Second\n3. Third"))

# Test quote
   # print(block_to_block_type(">Line one\n>Line two"))

# Test code
   print(block_to_block_type("```\nsome code\nmore code\n```"))

   
main()