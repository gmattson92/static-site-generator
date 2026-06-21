from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = 'plain'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url):
            return True
        else:
            return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_type_to_tag(text_type):
    d_text_type_to_tag = {TextType.PLAIN: None,
                          TextType.BOLD: 'b',
                          TextType.ITALIC: 'i',
                          TextType.CODE: 'code',
                          TextType.LINK: 'a',
                          TextType.IMAGE: 'img'}
    return d_text_type_to_tag[text_type]


def textnode_to_htmlnode(text_node: TextNode) -> LeafNode:
    if text_node.text_type not in TextType:
        raise ValueError(f'Invalid text type {text_node.text_type}')
    tag = text_type_to_tag(text_node.text_type)
    value = text_node.text
    props = None
    if text_node.text_type == TextType.LINK:
        props = {'href': text_node.url}
    if text_node.text_type == TextType.IMAGE:
        value = ''
        props = {'src': text_node.url, 'alt': text_node.text}
    return LeafNode(tag, value, props)
