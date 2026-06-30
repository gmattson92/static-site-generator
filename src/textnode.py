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


def split_node_delimiter(node: TextNode,
                         delimiter: str) -> list[TextNode]:
    """
    Splits text with inline Markdown formatting into component TextNode
    objects. Cannot handle nested inline elements,
    e.g. "_some **bold** italic text_"
    """
    if delimiter not in ['**', '_', '`']:
        raise ValueError(f'Invalid delimiter {delimiter}; '
                         'split_node_delimiter handles only bold ("**"), '
                         'italic ("_") and code ("`") delimiters.')
    # If node is not plain text, do nothing to it
    if node.text_type != TextType.PLAIN:
        return [node]
    d_delimiter_to_text_type = {'**': TextType.BOLD,
                                '_': TextType.ITALIC,
                                '`': TextType.CODE}
    text_type = d_delimiter_to_text_type[delimiter]
    new_nodes = []
    parts = node.text.split(delimiter)
    # Ensure we have a matching closing delimiter for each opening one
    if len(parts) % 2 != 1:
        raise ValueError(f'Invalid Markdown string {node.text}; '
                         f'found opening delimiter {delimiter} with no '
                         'matching close')
    for i, part in enumerate(parts):
        # Don't create a new node for empty strings
        if part == '':
            continue
        # Ensure only text between delimiters is converted to text_type
        if i % 2 == 1:
            this_text_type = text_type
        else:
            this_text_type = TextType.PLAIN
        new_node = TextNode(part, this_text_type, node.url)
        new_nodes.append(new_node)
    return new_nodes


def split_nodes_delimiter(old_nodes: list[TextNode],
                          delimiter: str) -> list[TextNode]:
    """
    Splits TextNode objects with inline Markdown formatting into component
    TextNode objects. Cannot handle nested inline elements,
    e.g. "_some **bold** italic text_"
    """
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_node_delimiter(node, delimiter))
    return new_nodes
