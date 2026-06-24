import unittest
import textnode as tn


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = tn.TextNode('This is a text node',
                            tn.TextType.BOLD, 'boot.dev')
        node2 = tn.TextNode('This is a text node',
                            tn.TextType.BOLD, 'boot.dev')
        self.assertEqual(node1, node2)

    def test_neq1(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a different text node', tn.TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a text node', tn.TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq3(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a different text node',
                            tn.TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq4(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a text node',
                            tn.TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq5(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a different text node',
                            tn.TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq6(self):
        node1 = tn.TextNode('This is a text node', tn.TextType.BOLD)
        node2 = tn.TextNode('This is a different text node',
                            tn.TextType.ITALIC, 'boot.dev')
        self.assertNotEqual(node1, node2)


class TestTextToHTML(unittest.TestCase):
    def test_plain(self):
        node = tn.TextNode('This is some plain text', tn.TextType.PLAIN)
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is some plain text')
        self.assertEqual(html_node.to_html(), 'This is some plain text')

    def test_bold(self):
        node = tn.TextNode('This is some bold text', tn.TextType.BOLD)
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is some bold text')
        html_str = '<b>This is some bold text</b>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_italic(self):
        node = tn.TextNode('This is some italic text', tn.TextType.ITALIC)
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'This is some italic text')
        html_str = '<i>This is some italic text</i>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_code(self):
        node = tn.TextNode('This is some code', tn.TextType.CODE)
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'This is some code')
        html_str = '<code>This is some code</code>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_link(self):
        node = tn.TextNode('This is a link', tn.TextType.LINK, 'boot.dev')
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'This is a link')
        self.assertEqual(html_node.props, {'href': 'boot.dev'})
        html_str = '<a href="boot.dev">This is a link</a>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_image(self):
        node = tn.TextNode('This is an image', tn.TextType.IMAGE,
                           'boot.dev/dummy.jpg')
        html_node = tn.textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props,
                         {'src': 'boot.dev/dummy.jpg',
                          'alt': 'This is an image'})
        html_str = '<img src="boot.dev/dummy.jpg" alt="This is an image">'
        self.assertEqual(html_node.to_html(), html_str)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_plain(self):
        node = tn.TextNode('This is some plain text', tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_delimiter([node], '**')
        self.assertListEqual(new_nodes, [node])

    def test_non_plain(self):
        node = tn.TextNode('This is some plain text', tn.TextType.LINK)
        new_nodes = tn.split_nodes_delimiter([node], '**')
        self.assertListEqual(new_nodes, [node])

    def test_bold(self):
        node = tn.TextNode('This is some **bold** text', tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_delimiter([node], '**')
        correct = [
            tn.TextNode('This is some ', tn.TextType.PLAIN),
            tn.TextNode('bold', tn.TextType.BOLD),
            tn.TextNode(' text', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_italic(self):
        node = tn.TextNode('This is some _italic_ text', tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_delimiter([node], '_')
        correct = [
            tn.TextNode('This is some ', tn.TextType.PLAIN),
            tn.TextNode('italic', tn.TextType.ITALIC),
            tn.TextNode(' text', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_code(self):
        node = tn.TextNode('This is some `code`', tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_delimiter([node], '`')
        correct = [
            tn.TextNode('This is some ', tn.TextType.PLAIN),
            tn.TextNode('code', tn.TextType.CODE)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_multi(self):
        old_nodes = [
            tn.TextNode('This is some **bold text**, ', tn.TextType.PLAIN),
            tn.TextNode('followed by some `code`, ', tn.TextType.PLAIN),
            tn.TextNode('then a link', tn.TextType.PLAIN, 'boot.dev')
        ]
        new_nodes = tn.split_nodes_delimiter(old_nodes, '`')
        new_nodes = tn.split_nodes_delimiter(new_nodes, '**')
        correct = [
            tn.TextNode('This is some ', tn.TextType.PLAIN),
            tn.TextNode('bold text', tn.TextType.BOLD),
            tn.TextNode(', ', tn.TextType.PLAIN),
            tn.TextNode('followed by some ', tn.TextType.PLAIN),
            tn.TextNode('code', tn.TextType.CODE),
            tn.TextNode(', ', tn.TextType.PLAIN),
            tn.TextNode('then a link', tn.TextType.PLAIN, 'boot.dev')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_concat(self):
        original_text = ('This is some **bold text**, followed by some `code`'
                         ', then a link')
        node = tn.TextNode(original_text, tn.TextType.PLAIN, 'boot.dev')
        new_nodes = tn.split_nodes_delimiter([node], '`')
        new_nodes = tn.split_nodes_delimiter(new_nodes, '**')
        correct = [
            tn.TextNode('This is some ', tn.TextType.PLAIN, 'boot.dev'),
            tn.TextNode('bold text', tn.TextType.BOLD, 'boot.dev'),
            tn.TextNode(', followed by some ', tn.TextType.PLAIN, 'boot.dev'),
            tn.TextNode('code', tn.TextType.CODE, 'boot.dev'),
            tn.TextNode(', then a link', tn.TextType.PLAIN, 'boot.dev'),
        ]
        self.assertListEqual(new_nodes, correct)


class TestImageLinkExtraction(unittest.TestCase):
    def test_image_1(self):
        search_text = ('This is an example with a '
                       '![rick roll](https://i.imgur.com/aKaOqIh.gif) and '
                       '![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)')
        image_info = tn.extract_markdown_images(search_text)
        correct = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                   ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(image_info, correct)

    def test_image_2(self):
        # Require that images have a source -- but alt text is not necessary
        search_text = ('This is a bad example with a '
                       '![](https://i.imgur.com/aKaOqIh.gif) and '
                       '![obi wan]()')
        image_info = tn.extract_markdown_images(search_text)
        correct = [('', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertListEqual(image_info, correct)

    def test_link_1(self):
        search_text = ('This is text with links to '
                       '[rick roll](https://i.imgur.com/aKaOqIh.gif) and '
                       '[obi wan](https://i.imgur.com/fJRm4Vk.jpeg)')
        link_info = tn.extract_markdown_links(search_text)
        correct = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
                   ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(link_info, correct)

    def test_link_2(self):
        # Require that links have both display text and a URL
        search_text = ('This is a bad example with links to '
                       '[](https://i.imgur.com/aKaOqIh.gif) and '
                       '[obi wan]()')
        link_info = tn.extract_markdown_links(search_text)
        correct = []
        self.assertListEqual(link_info, correct)

    def test_mixed(self):
        search_text = ('This is an example with an image '
                       '![image](https://i.imgur.com/aKaOqIh.gif) and '
                       'a [link](https://i.imgur.com/fJRm4Vk.jpeg)')
        image_info = tn.extract_markdown_images(search_text)
        image_correct = [('image', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertListEqual(image_info, image_correct)
        link_info = tn.extract_markdown_links(search_text)
        link_correct = [('link', 'https://i.imgur.com/fJRm4Vk.jpeg')]
        self.assertListEqual(link_info, link_correct)


class TestSplitNodesImage(unittest.TestCase):
    def test_plain(self):
        text = 'This is some plain text'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_image_at_beginning(self):
        text = '![alt text](some.url) this text begins with an image'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_image([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url'),
            tn.TextNode(' this text begins with an image', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_at_end(self):
        text = 'this text ends with an image ![alt text](some.url)'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_image([node])
        correct = [
            tn.TextNode('this text ends with an image ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.IMAGE, 'some.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_image_at_beginning_and_end(self):
        text = ('![alt text](some.url) this text begins with an image'
                ' and ends with another ![other alt text](other.url)')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_image([node])
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
        new_nodes = tn.split_nodes_image([node])
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
        new_nodes = tn.split_nodes_image(old_nodes)
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
        new_nodes = tn.split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_link_at_beginning(self):
        text = '[alt text](some.url) this text begins with a link'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_link([node])
        correct = [
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url'),
            tn.TextNode(' this text begins with a link', tn.TextType.PLAIN)
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_at_end(self):
        text = 'this text ends with a link [alt text](some.url)'
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_link([node])
        correct = [
            tn.TextNode('this text ends with a link ', tn.TextType.PLAIN),
            tn.TextNode('alt text', tn.TextType.LINK, 'some.url')
        ]
        self.assertListEqual(new_nodes, correct)

    def test_link_at_beginning_and_end(self):
        text = ('[alt text](some.url) this text begins with a link'
                ' and ends with another [other alt text](other.url)')
        node = tn.TextNode(text, tn.TextType.PLAIN)
        new_nodes = tn.split_nodes_link([node])
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
        new_nodes = tn.split_nodes_link([node])
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
        new_nodes = tn.split_nodes_link(old_nodes)
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


if __name__ == '__main__':
    unittest.main()
