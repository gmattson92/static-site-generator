import re
from enum import Enum
from textnode import (TextNode, TextType, split_nodes_delimiter,
                      textnode_to_htmlnode)
from htmlnode import ParentNode


def extract_markdown_images(text: str) -> list[tuple]:
    """
    Parses text for Markdown image tags and returns a list of
    (alt text, URL) tuples.
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


def inline_markdown_to_textnodes(text: str) -> list[TextNode]:
    """
    Converts a Markdown string containing inline formatting, images and links
    into component TextNode objects.
    """
    starting_node = TextNode(text, TextType.PLAIN)
    output = split_nodes_delimiter([starting_node], '**')
    output = split_nodes_delimiter(output, '`')
    output = split_nodes_delimiter(output, '_')
    output = split_nodes_image(output)
    output = split_nodes_link(output)
    return output


def markdown_to_blocks(full_markdown_string: str) -> list[str]:
    raw_blocks = full_markdown_string.split('\n\n')
    stripped_blocks = []
    for block in raw_blocks:
        if not block.strip():
            continue
        else:
            stripped_blocks.append(block.strip())
    return stripped_blocks


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'


def is_heading(block: str) -> bool:
    search_str = r'^#{1,6} \w+'
    m = re.search(search_str, block)
    if m:
        return True
    else:
        return False


def is_quote(lines: list[str]) -> bool:
    for line in lines:
        if len(line) < 1:
            return False
        if line[0] != '>':
            return False
    return True


def is_unordered_list(lines: list[str]) -> bool:
    for line in lines:
        if len(line) < 2:
            return False
        if line[0:2] != '- ':
            return False
    return True


def is_ordered_list(lines: list[str]) -> bool:
    current_number = 1
    for line in lines:
        if len(line) < 3:
            return False
        num_length = len(str(current_number))
        try:
            leading_number = int(line[:num_length])
        except ValueError:
            return False
        if leading_number != current_number:
            return False
        if line[num_length:num_length+1] != '.':
            return False
        current_number += 1
    return True


def markdown_block_to_block_type(block: str) -> BlockType:
    """
    Reads a string corresponding to a single Markdown block and returns the
    corresponding BlockType. Assumes leading and trailing whitespace have been
    stripped.
    """
    lines = block.split('\n')
    # Headings
    if is_heading(block):
        return BlockType.HEADING
    # Multiline code
    if len(block) > 3:
        if (block[0:4] == '```\n' and block[-4:] == '\n```'):
            return BlockType.CODE
    # Multiline quotes
    if is_quote(lines):
        return BlockType.QUOTE
    # Unordered lists
    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    # Ordered lists
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    # If none of the above, it's a paragraph
    return BlockType.PARAGRAPH


def get_heading_number(heading_block: str) -> int:
    """
    Parses a Markdown heading string and returns the corresponding HTML
    heading number.
    """
    search_str = r'^(#{1,6})'
    m = re.search(search_str, heading_block)
    if m:
        return len(m.group(0))
    else:
        raise ValueError('get_heading_number called on non-heading block =\n'
                         f'{heading_block}')


def get_parent_html_tag(block: str) -> str:
    """
    Parses a Markdown block and returns the corresponding HTML tag.
    """
    block_type = markdown_block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        tag = 'p'
    elif block_type == BlockType.HEADING:
        num = get_heading_number(block)
        tag = f'h{num}'
    elif block_type == BlockType.CODE:
        tag = 'pre'
    elif block_type == BlockType.QUOTE:
        tag = 'blockquote'
    elif block_type == BlockType.UNORDERED_LIST:
        tag = 'ul'
    elif block_type == BlockType.ORDERED_LIST:
        tag = 'ol'
    else:
        raise ValueError('Invalid block type {block_type}')
    return tag


def get_paragraph_node(block):
    tag = get_parent_html_tag(block)
    textnodes = inline_markdown_to_textnodes(block)
    children = [textnode_to_htmlnode(node) for node in textnodes]
    return ParentNode(tag, children)


def get_heading_node(heading_block):
    tag = get_parent_html_tag(heading_block)
    text = heading_block.strip('# ')
    textnodes = inline_markdown_to_textnodes(text)
    children = [textnode_to_htmlnode(node) for node in textnodes]
    return ParentNode(tag, children)


def get_code_node(code_block):
    tag = get_parent_html_tag(code_block)
    text = code_block.strip('`')
    textnode = TextNode(text, TextType.CODE)
    htmlnode = textnode_to_htmlnode(textnode)
    children = [htmlnode]
    return ParentNode(tag, children)


def get_quote_node(quote_block):
    tag = get_parent_html_tag(quote_block)
    children = []
    lines = quote_block.split('\n')
    for line in lines:
        text = line.strip('> ')
        text += '\n'
        textnodes = inline_markdown_to_textnodes(text)
        htmlnodes = [textnode_to_htmlnode(node) for node in textnodes]
        children.extend(htmlnodes)
    return ParentNode(tag, children)


def get_unordered_list_node(ul_block):
    tag = get_parent_html_tag(ul_block)
    list_children = []
    lines = ul_block.split('\n')
    for line in lines:
        htmlnodes = []
        text = line.strip('- ')
        textnodes = inline_markdown_to_textnodes(text)
        for node in textnodes:
            # node.text = '<li>' + node.text + '</li>'
            htmlnodes.append(textnode_to_htmlnode(node))
        linenode = ParentNode('li', htmlnodes)
        list_children.append(linenode)
    return ParentNode(tag, list_children)


def get_ordered_list_node(ol_block):
    tag = get_parent_html_tag(ol_block)
    list_children = []
    lines = ol_block.split('\n')
    for line in lines:
        htmlnodes = []
        starting_index = line.find(' ') + 1
        text = line[starting_index:]
        textnodes = inline_markdown_to_textnodes(text)
        for node in textnodes:
            # node.text = '<li>' + node.text + '</li>'
            htmlnodes.append(textnode_to_htmlnode(node))
        linenode = ParentNode('li', htmlnodes)
        list_children.append(linenode)
    return ParentNode(tag, list_children)


def block_to_parent_node(block: str) -> ParentNode:
    block_type = markdown_block_to_block_type(block)
    d_block_type_to_fn = {
        BlockType.PARAGRAPH: get_paragraph_node,
        BlockType.HEADING: get_heading_node,
        BlockType.CODE: get_code_node,
        BlockType.QUOTE: get_quote_node,
        BlockType.UNORDERED_LIST: get_unordered_list_node,
        BlockType.ORDERED_LIST: get_ordered_list_node
    }
    if block_type not in d_block_type_to_fn:
        raise ValueError(f'Invalid block type {block_type}')
    return d_block_type_to_fn[block_type](block)


def markdown_to_htmlnode(markdown: str) -> ParentNode:
    """
    Parses a string representing a full Markdown file and returns an HTMLNode
    whose text representation corresponds to the full HTML code required to
    display the Markdown file in a browser.
    """
    blocks = markdown_to_blocks(markdown)
    parents = []
    for block in blocks:
        parent_node = block_to_parent_node(block)
        parents.append(parent_node)
    return ParentNode('div', parents)
