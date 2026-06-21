import unittest
from textnode import TextNode, TextType, textnode_to_htmlnode


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        node2 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        self.assertEqual(node1, node2)

    def test_neq1(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node', TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_neq2(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq3(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node', TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_neq4(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq5(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node',
                         TextType.BOLD, 'boot.dev')
        self.assertNotEqual(node1, node2)

    def test_neq6(self):
        node1 = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a different text node',
                         TextType.ITALIC, 'boot.dev')
        self.assertNotEqual(node1, node2)


class TestTextToHTML(unittest.TestCase):
    def test_plain(self):
        node = TextNode('This is some plain text', TextType.PLAIN)
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, 'This is some plain text')
        self.assertEqual(html_node.to_html(), 'This is some plain text')

    def test_bold(self):
        node = TextNode('This is some bold text', TextType.BOLD)
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'This is some bold text')
        html_str = '<b>This is some bold text</b>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_italic(self):
        node = TextNode('This is some italic text', TextType.ITALIC)
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'This is some italic text')
        html_str = '<i>This is some italic text</i>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_code(self):
        node = TextNode('This is some code', TextType.CODE)
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'This is some code')
        html_str = '<code>This is some code</code>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_link(self):
        node = TextNode('This is a link', TextType.LINK, 'boot.dev')
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'This is a link')
        self.assertEqual(html_node.props, {'href': 'boot.dev'})
        html_str = '<a href="boot.dev">This is a link</a>'
        self.assertEqual(html_node.to_html(), html_str)

    def test_image(self):
        node = TextNode('This is an image', TextType.IMAGE,
                        'boot.dev/dummy.jpg')
        html_node = textnode_to_htmlnode(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props,
                         {'src': 'boot.dev/dummy.jpg',
                          'alt': 'This is an image'})
        html_str = '<img src="boot.dev/dummy.jpg" alt="This is an image">'
        self.assertEqual(html_node.to_html(), html_str)


if __name__ == '__main__':
    unittest.main()
