import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq1(self):
        node = HTMLNode('p', 'This is some text')
        props_str = ''
        self.assertEqual(node.props_to_html(), props_str)

    def test_eq2(self):
        node = HTMLNode('a', 'This is a link', None,
                        {'href': 'boot.dev'})
        props_str = ' href="boot.dev"'
        self.assertEqual(node.props_to_html(), props_str)

    def test_eq3(self):
        node = HTMLNode('a', 'This is a link', None,
                        {'href': 'boot.dev', 'target': '_blank'})
        props_str = ' href="boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), props_str)


class TestLeafNode(unittest.TestCase):
    def test_eq1(self):
        node = LeafNode('p', 'This is some text')
        html_str = '<p>This is some text</p>'
        self.assertEqual(node.to_html(), html_str)

    def test_eq2(self):
        node = LeafNode('a', 'This is a link', {'href': 'boot.dev'})
        html_str = '<a href="boot.dev">This is a link</a>'
        self.assertEqual(node.to_html(), html_str)


if __name__ == '__main__':
    unittest.main()
