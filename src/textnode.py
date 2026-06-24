import re
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


def extract_markdown_images(text: str) -> list[tuple]:
    """
    Parses text for Markdown image tags and returns a list of
    (alt_text, URL) tuples.
    """
    search_str = r'!\[([^\]]*)\]\(([^\)]+)\)'
    return re.findall(search_str, text)


def extract_markdown_links(text: str) -> list[tuple]:
    """
    Parses text for Markdown hyperlinks and returns a list of
    (link text, URL) tuples.
    """
    search_str = r'(?<!!)\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(search_str, text)


def split_node_image_or_link(node: TextNode,
                             split_str: str) -> list[TextNode]:
    """
    Splits text with Markdown images or links into component TextNode objects.
    If no image or link tags are found, returns [node] without changes.
    """
    if split_str == r'![':
        extract_fn = extract_markdown_images
        tag_type = TextType.IMAGE
    elif split_str == r'[':
        extract_fn = extract_markdown_links
        tag_type = TextType.LINK
    else:
        raise ValueError(f'Invalid split_str = {split_str}')

    tag_info = extract_fn(node.text)
    if not tag_info:
        return [node]
    new_nodes = []
    the_text = node.text
    tag_index = 0
    while the_text:
        # Split the text one chunk at a time
        parts = the_text.split(split_str, maxsplit=1)
        pre_text = parts[0]
        if pre_text:
            new_nodes.append(TextNode(pre_text, TextType.PLAIN))
        if len(parts) == 1:
            # No remaining text, stop here
            break
        remainder_text = parts[1]
        if not remainder_text:
            # Remainder is empty, stop here
            break
        # remainder_text now begins with a tag
        # Next create the node for this image/link
        tag_node = TextNode(tag_info[tag_index][0],
                            tag_type,
                            tag_info[tag_index][1])
        new_nodes.append(tag_node)
        # Find the first occurence of ')' in the remainer text --
        # this is where the tag ends
        end_tag_index = (remainder_text.find(r')')
                         + len(pre_text)
                         + len(split_str))
        the_text = the_text[end_tag_index+1:]
        tag_index += 1
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNode objects with Markdown images into component
    TextNode objects. Any nodes without image tags are included in the returned
    list as-is.
    """
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_node_image_or_link(node, r'!['))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNode objects with Markdown links into component
    TextNode objects. Any nodes without link tags are included in the returned
    list as-is.
    """
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(split_node_image_or_link(node, r'['))
    return new_nodes
