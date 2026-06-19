import unittest
from htmlnode import HTMLNode


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


if __name__ == '__main__':
    unittest.main()
