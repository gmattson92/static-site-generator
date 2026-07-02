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
        html_str = '<img src="boot.dev/dummy.jpg" alt="This is an image"/>'
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


if __name__ == '__main__':
    unittest.main()
