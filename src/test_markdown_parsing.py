import unittest
import textnode as tn
import markdown_parsing as mp


class TestImageLinkExtraction(unittest.TestCase):
    def test_image_1(self):
        search_text = ('This is an example with a '
                       '![rick roll](https://i.imgur.com/aKaOqIh.gif) and '
                       '![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)')
        image_info = mp.extract_markdown_images(search_text)
        correct = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                   ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(image_info, correct)

    def test_image_2(self):
        # Require that images have a source -- but alt text is not necessary
        search_text = ('This is a bad example with a '
                       '![](https://i.imgur.com/aKaOqIh.gif) and '
                       '![obi wan]()')
        image_info = mp.extract_markdown_images(search_text)
        correct = [('', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertListEqual(image_info, correct)

    def test_link_1(self):
        search_text = ('This is text with links to '
                       '[rick roll](https://i.imgur.com/aKaOqIh.gif) and '
                       '[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)')
        link_info = mp.extract_markdown_links(search_text)
        correct = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                   ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(link_info, correct)

    def test_link_2(self):
        # Require that links have both display text and a URL
        search_text = ('This is a bad example with links to '
                       '[](https://i.imgur.com/aKaOqIh.gif) and '
                       '[obi wan]()')
        link_info = mp.extract_markdown_links(search_text)
        correct = []
        self.assertListEqual(link_info, correct)

    def test_mixed(self):
        search_text = ('This is an example with an image '
                       '![image](https://i.imgur.com/aKaOqIh.gif) and '
                       'a [link](https://i.imgur.com/fJRm4Vk.jpeg)')
        image_info = mp.extract_markdown_images(search_text)
        image_correct = [('image', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertListEqual(image_info, image_correct)
        link_info = mp.extract_markdown_links(search_text)
        link_correct = [('link', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(link_info, link_correct)


class TestSplitNodesImage(unittest.TestCase):
    def test_plain(self):
        text = 'This is some plain text'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_image_at_beginning(self):
        text = '![alt text](some.url) this text begins with an image'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_image([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url'),
            tn.TextNode(' this text begins with an image', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_at_end(self):
        text = 'this text ends with an image ![alt text](some.url)'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_image([node])
        correct = [
            tn.TextNode('this text ends with an image ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_at_beginning_and_end(self):
        text = ('![alt text](some.url) this text begins with an image'
                ' and ends with another ![other alt text](other.url)')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_image([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url'),
            tn.TextNode(' this text begins with an image'
                        ' and ends with another ', tn.TextType.PLAIN),
            tn.TextNode('other alt text', tn.TextType.IMAGE, 'other.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_in_middle(self):
        text = ('this text has an image ![alt text](some.url) in the middle')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_image([node])
        correct = [
            tn.TextNode('this text has an image ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url'),
            tn.TextNode(' in the middle', tn.TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_multi(self):
        text1 = ('this text has an image ![alt text](some.url) in the middle')
        node1 = tn.TextNode(text1, tn.TextType.PLAIN)
        text2 = ('this text does not have an image')
        node2 = tn.TextNode(text2, tn.TextType.PLAIN)
        text3 = ('this text has two images![second text](second.url)'
                 '![third text](third.url)in the middle')
        node3 = tn.TextNode(text3, tn.TextType.PLAIN)
        old_nodes = [node1, node2, node3]
        new_nodes = mp.split_nodes_image(old_nodes)
        correct = [
            tn.TextNode('this text has an image ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url'),
            tn.TextNode(' in the middle', tn.TextType.PLAIN),
            tn.TextNode('this text does not have an image', tn.TextType.PLAIN),
            tn.TextNode('this text has two images', tn.TextType.PLAIN),
            tn.TextNode('second text', tn.TextType.IMAGE, 'second.url'),
            tn.TextNode('third text', tn.TextType.IMAGE, 'third.url'),
            tn.TextNode('in the middle', tn.TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, correct)


class TestSplitNodesLink(unittest.TestCase):
    def test_plain(self):
        text = 'This is some plain text'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_link_at_beginning(self):
        text = '[alt text](some.url) this text begins with a link'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_link([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url'),
            tn.TextNode(' this text begins with a link', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_at_end(self):
        text = 'this text ends with a link [alt text](some.url)'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_link([node])
        correct = [
            tn.TextNode('this text ends with a link ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_at_beginning_and_end(self):
        text = ('[alt text](some.url) this text begins with a link'
                ' and ends with another [other alt text](other.url)')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_link([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url'),
            tn.TextNode(' this text begins with a link'
                        ' and ends with another ', tn.TextType.PLAIN),
            tn.TextNode('other alt text', tn.TextType.LINK, 'other.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_in_middle(self):
        text = ('this text has a link [alt text](some.url) in the middle')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = mp.split_nodes_link([node])
        correct = [
            tn.TextNode('this text has a link ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url'),
            tn.TextNode(' in the middle', tn.TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_multi(self):
        text1 = ('this text has a link [alt text](some.url) in the middle')
        node1 = tn.TextNode(text1, tn.TextType.PLAIN)
        text2 = ('this text does not have a link')
        node2 = tn.TextNode(text2, tn.TextType.PLAIN)
        text3 = ('this text has two links[second text](second.url)'
                 '[third text](third.url)in the middle')
        node3 = tn.TextNode(text3, tn.TextType.PLAIN)
        old_nodes = [node1, node2, node3]
        new_nodes = mp.split_nodes_link(old_nodes)
        correct = [
            tn.TextNode('this text has a link ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url'),
            tn.TextNode(' in the middle', tn.TextType.PLAIN),
            tn.TextNode('this text does not have a link', tn.TextType.PLAIN),
            tn.TextNode('this text has two links', tn.TextType.PLAIN),
            tn.TextNode('second text', tn.TextType.LINK, 'second.url'),
            tn.TextNode('third text', tn.TextType.LINK, 'third.url'),
            tn.TextNode('in the middle', tn.TextType.PLAIN),
        ]
        self.assertListEqual(new_nodes, correct)


class TestSplitInlineMarkdown(unittest.TestCase):
    def test_plain(self):
        text = 'This is some plain text'
        new_nodes = mp.inline_markdown_to_textnodes(text)
        correct = [tn.TextNode(text, tn.TextType.PLAIN)]
        self.assertListEqual(new_nodes, correct)

    def test_all(self):
        text = ('This is **text** with an _italic_ word and a `code block` '
                'and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) '
                'and a [link](https://boot.dev)')
        new_nodes = mp.inline_markdown_to_textnodes(text)
        correct = [
            tn.TextNode("This is ", tn.TextType.PLAIN),
            tn.TextNode("text", tn.TextType.BOLD),
            tn.TextNode(" with an ", tn.TextType.PLAIN),
            tn.TextNode("italic", tn.TextType.ITALIC),
            tn.TextNode(" word and a ", tn.TextType.PLAIN),
            tn.TextNode("code block", tn.TextType.CODE),
            tn.TextNode(" and an ", tn.TextType.PLAIN),
            tn.TextNode("obi wan image", tn.TextType.IMAGE,
                        "https://i.imgur.com/fJRm4Vk.jpeg"),
            tn.TextNode(" and a ", tn.TextType.PLAIN),
            tn.TextNode("link", tn.TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(new_nodes, correct)

    def test_nested_underscore(self):
        text = 'This is **text** with an _italic_ word and a `code_block`'
        new_nodes = mp.inline_markdown_to_textnodes(text)
        correct = [
            tn.TextNode("This is ", tn.TextType.PLAIN),
            tn.TextNode("text", tn.TextType.BOLD),
            tn.TextNode(" with an ", tn.TextType.PLAIN),
            tn.TextNode("italic", tn.TextType.ITALIC),
            tn.TextNode(" word and a ", tn.TextType.PLAIN),
            tn.TextNode("code_block", tn.TextType.CODE),
        ]
        self.assertListEqual(new_nodes, correct)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_plain(self):
        text = '''
This is some plain text.

This is a new paragraph.
This is the same paragraph on a new line.

This third paragraph should be the third block.
        '''
        blocks = mp.markdown_to_blocks(text)
        correct = [
            'This is some plain text.',
            ('This is a new paragraph.\n'
             'This is the same paragraph on a new line.'),
            'This third paragraph should be the third block.']
        self.assertListEqual(blocks, correct)

    def test_with_inline(self):
        text = '''
This is some **bold** text.

This is a new paragraph, with _italics_.
This is the same paragraph on a new line.

This third paragraph has an image ![alt text](some.url) then more text.
        '''
        blocks = mp.markdown_to_blocks(text)
        correct = [
            'This is some **bold** text.',
            ('This is a new paragraph, with _italics_.\n'
             'This is the same paragraph on a new line.'),
            ('This third paragraph has an image '
             '![alt text](some.url) then more text.')]
        self.assertListEqual(blocks, correct)

    def test_extra_whitespace(self):
        text = '''

This is some plain text.


This is a new paragraph.
    This is the same paragraph on a new line.



This third paragraph should be the third block.

        '''
        blocks = mp.markdown_to_blocks(text)
        correct = [
            'This is some plain text.',
            ('This is a new paragraph.\n'
             '    This is the same paragraph on a new line.'),
            'This third paragraph should be the third block.']
        self.assertListEqual(blocks, correct)


if __name__ == '__main__':
    unittest.main()
