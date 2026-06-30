import re
from textnode import TextNode, TextType, split_nodes_delimiter


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
