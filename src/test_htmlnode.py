import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_no_children(self):
        children = []
        node = ParentNode('p', children)
        try:
            html_str = node.to_html()
        except ValueError:
            html_str = ''
        self.assertEqual(html_str, '')

    def test_eq1(self):
        children = [LeafNode('b', 'some bold text')]
        node = ParentNode('p', children)
        html_str = '<p><b>some bold text</b></p>'
        self.assertEqual(node.to_html(), html_str)

    def test_eq2(self):
        children = [LeafNode('b', 'some bold text'),
                    LeafNode(None, 'some plain text'),
                    LeafNode('i', 'some italic text')]
        node = ParentNode('p', children)
        html_str = ('<p><b>some bold text</b>some plain text'
                    '<i>some italic text</i></p>')
        self.assertEqual(node.to_html(), html_str)

    def test_nested1(self):
        grandchild = LeafNode('i', 'some bold italic text')
        child = ParentNode('b', [grandchild])
        node = ParentNode('p', [child])
        html_str = '<p><b><i>some bold italic text</i></b></p>'
        self.assertEqual(node.to_html(), html_str)

    def test_nested2(self):
        grandchild1 = LeafNode('i', 'some bold italic text')
        grandchild2 = LeafNode('a', 'a bold link', {'href': 'boot.dev'})
        child = ParentNode('b', [grandchild1, grandchild2])
        node = ParentNode('p', [child])
        html_str = ('<p><b><i>some bold italic text</i>'
                    '<a href="boot.dev">a bold link</a></b></p>')
        self.assertEqual(node.to_html(), html_str)


if __name__ == '__main__':
    unittest.main()
